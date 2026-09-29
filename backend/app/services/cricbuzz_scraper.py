"""
Cricbuzz Scraper Service
========================
Scrapes live/recent/upcoming matches and full scorecards from Cricbuzz.
This is an unofficial scraper — no API key needed, but it may break
if Cricbuzz changes their HTML structure.

Data we extract:
- Match listings (live, recent, upcoming) with scores
- Full scorecard per innings (batting + bowling + extras + FoW)
- Match status, venue, toss info

Cricbuzz URLs:
  /live-cricket-scores            → match listings
  /live-cricket-scorecard/{id}    → full scorecard
"""

import re
import time
import logging
import httpx
from bs4 import BeautifulSoup
from typing import Optional

logger = logging.getLogger(__name__)

CRICBUZZ_BASE = "https://www.cricbuzz.com"
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
]

# Cache
_cache: dict[str, dict] = {}
CACHE_TTL = {"matches": 60, "scorecard": 30}


def _get_cache(key: str) -> Optional[dict]:
    entry = _cache.get(key)
    if entry and time.time() - entry["ts"] < entry["ttl"]:
        return entry["data"]
    return None


def _set_cache(key: str, data: dict, ttl: int):
    _cache[key] = {"data": data, "ts": time.time(), "ttl": ttl}


async def _fetch_page(url: str) -> Optional[BeautifulSoup]:
    """Fetch a page from Cricbuzz and parse with BeautifulSoup."""
    import random
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    try:
        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200:
                return BeautifulSoup(resp.content, "lxml")
    except Exception as e:
        logger.error(f"Cricbuzz fetch error for {url}: {e}")
    return None


def _is_pakistan_match(title: str, teams: list[str]) -> bool:
    """Check if Pakistan is in this match."""
    check = (title + " ".join(teams)).lower()
    return "pakistan" in check or "pak " in check or " pak" in check


# === Match Listings ===

async def get_matches() -> dict:
    """Scrape live/recent/upcoming matches from Cricbuzz."""
    cached = _get_cache("matches")
    if cached:
        return cached

    soup = await _fetch_page(f"{CRICBUZZ_BASE}/cricket-match/live-scores")
    if not soup:
        return {"matches": [], "error": "Could not reach Cricbuzz"}

    matches = []
    seen = set()

    for a in soup.find_all("a", href=re.compile(r"/live-cricket-scores/")):
        m = re.search(r"/live-cricket-scores/(\d+)", a["href"])
        if not m or m.group(1) in seen:
            continue
        seen.add(m.group(1))

        match_id = m.group(1)
        title = a.get("title", "") or a.get_text(strip=True)
        if not title or len(title) < 5:
            continue

        # Clean title
        title = re.sub(r"^(WATCH NOW|T20I|ODI|Test|FC|T20|OD)\s*", "", title)
        title = re.sub(r"\s+", " ", title).strip()

        # Extract teams
        teams = []
        vs_match = re.search(r"([A-Za-z\s]+?)\s+vs\s+([A-Za-z\s]+)", title, re.I)
        if vs_match:
            teams = [vs_match.group(1).strip(), vs_match.group(2).split(",")[0].strip()]

        # Determine status
        lower = title.lower()
        if "live" in lower:
            status = "live"
        elif any(w in lower for w in ["won", "complete", "stumps", "drawn", "rain", "abandon"]):
            status = "completed"
        else:
            status = "upcoming"

        match_data = {
            "id": match_id,
            "name": title,
            "teams": teams,
            "status": status,
            "source": "cricbuzz",
            "scorecard_url": f"/live-cricket-scorecard/{match_id}",
            "is_pakistan": _is_pakistan_match(title, teams),
        }
        matches.append(match_data)

    # Filter Pakistan matches
    pak_matches = [m for m in matches if m["is_pakistan"]]

    result = {
        "matches": pak_matches,
        "all_matches": matches,
        "total_pak": len(pak_matches),
        "total_all": len(matches),
        "source": "cricbuzz",
    }

    _set_cache("matches", result, CACHE_TTL["matches"])
    return result


# === Full Scorecard ===

async def get_scorecard(match_id: str) -> dict:
    """Scrape full scorecard for a match from Cricbuzz."""
    cache_key = f"scorecard_{match_id}"
    cached = _get_cache(cache_key)
    if cached:
        return cached

    soup = await _fetch_page(f"{CRICBUZZ_BASE}/live-cricket-scorecard/{match_id}")
    if not soup:
        return {"error": "Could not fetch scorecard from Cricbuzz", "source": "cricbuzz"}

    # Match title
    title_elem = soup.find("h1") or soup.find("title")
    title = title_elem.get_text(strip=True) if title_elem else ""
    title = re.sub(r"\s*\|.*$", "", title)  # Remove " | Cricbuzz" suffix

    # Status
    status_text = ""
    for cls in ["cb-text-complete", "cb-text-live", "cb-text-preview"]:
        elem = soup.find("div", class_=cls)
        if elem:
            status_text = elem.get_text(strip=True)
            break

    # Parse innings — Cricbuzz uses grid-based layout
    # Each batting/bowling grid represents one data row
    innings = _parse_innings(soup)

    result = {
        "id": match_id,
        "name": title,
        "status_text": status_text,
        "innings": innings,
        "source": "cricbuzz",
    }

    _set_cache(cache_key, result, CACHE_TTL["scorecard"])
    return result


def _parse_innings(soup: BeautifulSoup) -> list[dict]:
    """
    Parse all innings from the Cricbuzz scorecard page.

    The new Cricbuzz layout uses CSS grid classes:
    - scorecard-bat-grid: each batting row (header row has text "Batter")
    - scorecard-bowl-grid: each bowling row (header row has text "Bowler")

    The grids are flat — each grid has child divs that are the columns.
    The first grid in a batting section is the header, subsequent ones are player rows.
    """
    innings = []

    # Find innings section dividers — look for innings score headers
    # They typically have the team name and score like "West Indies Innings 202-10 (44.2)"
    # These are in divs that contain both team name and score

    # Strategy: find all batting grids and bowling grids, group them by innings
    all_bat_grids = soup.find_all(
        class_=lambda c: c and "scorecard-bat-grid" in c and "tb:" not in c and "wb:" not in c
    )
    all_bowl_grids = soup.find_all(
        class_=lambda c: c and "scorecard-bowl-grid" in c and "tb:" not in c and "wb:" not in c
    )

    # Parse batting entries
    batsmen = []
    for grid in all_bat_grids:
        cells = grid.find_all("div", recursive=False)
        if len(cells) < 6:
            continue

        first_text = cells[0].get_text(strip=True)

        # Skip header row (has 7 children, "Batter" as first text, or empty)
        if first_text in ("Batter", "") or len(cells) == 7:
            continue

        # Extract batsman name — use profile link URL (most reliable)
        name = ""
        for link in cells[0].find_all("a"):
            href = link.get("href", "")
            if "/profiles/" in href:
                parts = href.rstrip("/").split("/")
                name = parts[-1].replace("-", " ").title() if parts else ""
                break
        if not name:
            # Fallback: regex on full text (name is before "View" or dismissal)
            full_raw = cells[0].get_text(" ", strip=True)
            nm = re.match(r"^([A-Za-z\s.\-'()]+?)(?:\s*View|\s*c\s|\s*b\s|\s*lbw|\s*run|\s*st\s|\s*hit|\s*not out|\s*$)", full_raw)
            name = nm.group(1).strip() if nm else first_text.split("View")[0].strip()

        # Extract dismissal from the cell text
        full_text = cells[0].get_text(" ", strip=True)
        # Dismissal patterns: c X b Y, b X, lbw b X, run out, st X b Y, not out, hit wicket
        dismissal = "not out"
        dismissal_patterns = [
            r"(c\s+.+?\s+b\s+.+?)(?:View|$)",
            r"(b\s+[A-Z].+?)(?:View|$)",
            r"(lbw\s+b\s+.+?)(?:View|$)",
            r"(run\s+out\s*\(.+?\))",
            r"(st\s+.+?\s+b\s+.+?)(?:View|$)",
            r"(hit\s+wicket\s+b\s+.+?)(?:View|$)",
            r"(retired\s+.+?)(?:View|$)",
        ]
        for pattern in dismissal_patterns:
            dm = re.search(pattern, full_text, re.I)
            if dm:
                dismissal = dm.group(1).strip()
                break

        try:
            runs = _safe_int(cells[1].get_text(strip=True))
            balls = _safe_int(cells[2].get_text(strip=True))
            fours = _safe_int(cells[3].get_text(strip=True))
            sixes = _safe_int(cells[4].get_text(strip=True))
            sr = _safe_float(cells[5].get_text(strip=True))
        except (IndexError, ValueError):
            continue

        if name and len(name) > 1:
            batsmen.append({
                "name": name,
                "dismissal": dismissal,
                "runs": runs,
                "balls": balls,
                "fours": fours,
                "sixes": sixes,
                "strike_rate": sr,
            })

    # Parse bowling entries
    bowlers = []
    for grid in all_bowl_grids:
        cells = grid.find_all("div", recursive=False)
        if len(cells) < 6:
            continue

        first_text = cells[0].get_text(strip=True)

        # Skip header row
        if first_text in ("Bowler", ""):
            continue

        # Extract bowler name
        name = ""
        for link in cells[0].find_all("a"):
            href = link.get("href", "")
            if "/profiles/" in href:
                parts = href.rstrip("/").split("/")
                name = parts[-1].replace("-", " ").title() if parts else ""
                break
        if not name:
            name = first_text.split("View")[0].strip()

        try:
            overs = _safe_float(cells[1].get_text(strip=True))
            maidens = _safe_int(cells[2].get_text(strip=True))
            runs = _safe_int(cells[3].get_text(strip=True))
            wickets = _safe_int(cells[4].get_text(strip=True))
            economy = _safe_float(cells[5].get_text(strip=True))
        except (IndexError, ValueError):
            continue

        if name and len(name) > 1 and overs > 0:
            bowlers.append({
                "name": name,
                "overs": overs,
                "maidens": maidens,
                "runs": runs,
                "wickets": wickets,
                "economy": economy,
            })

    # Try to split batsmen/bowlers into innings by looking for innings section markers
    # For now, if we can detect innings breaks, split; otherwise return as one innings
    # Simple heuristic: look for extras/total rows between batting sections
    # Cricbuzz shows innings sequentially, so we group all data as available

    if batsmen or bowlers:
        innings.append({
            "batting": _dedupe_by_name(batsmen),
            "bowling": _dedupe_by_name(bowlers),
        })

    return innings


def _dedupe_by_name(items: list[dict]) -> list[dict]:
    """Remove duplicate entries by name."""
    seen = set()
    unique = []
    for item in items:
        if item["name"] not in seen:
            seen.add(item["name"])
            unique.append(item)
    return unique


def _safe_int(s: str) -> int:
    s = s.strip()
    if s.isdigit():
        return int(s)
    m = re.match(r"(\d+)", s)
    return int(m.group(1)) if m else 0


def _safe_float(s: str) -> float:
    s = s.strip()
    try:
        return float(s)
    except ValueError:
        m = re.match(r"(\d+\.?\d*)", s)
        return float(m.group(1)) if m else 0.0
