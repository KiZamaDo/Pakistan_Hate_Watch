"""
CricAPI Integration Service
============================
Fetches real match data from api.cricapi.com (CricketData.org).

Free tier endpoints (100 requests/day):
  GET /v1/matches          - all matches with inline scores
  GET /v1/currentMatches   - live/current matches with inline scores
  GET /v1/match_info       - single match detail (scores, toss, winner, squads)

Paid-only (not used):
  GET /v1/match_scorecard  - full batting/bowling card (requires paid plan)

Response format from CricAPI:
{
  "apikey": "...",
  "data": [ ... ] or { ... },
  "status": "success" | "failure",
  "info": { "hitsToday": N, "hitsLimit": N, ... }
}

Match object fields:
  id, name, matchType, status, venue, date, dateTimeGMT,
  teams (array of 2 strings), teamInfo (array of {name, shortname, img}),
  score (array of {r, w, o, inning}),
  series_id, fantasyEnabled, bbbEnabled, hasSquad,
  matchStarted (bool), matchEnded (bool)

match_info additionally includes:
  tossWinner, tossChoice, matchWinner
"""

import os
import time
import httpx
from typing import Optional

CRICAPI_BASE = "https://api.cricapi.com/v1"

# --- In-memory cache ---
_cache: dict[str, dict] = {}
CACHE_TTL = {
    "current_matches": 60,
    "all_matches": 300,
    "match_info": 120,
}


def _get_api_key() -> str:
    return os.getenv("CRICKET_API_KEY", "")


def _get_cache(key: str) -> Optional[dict]:
    entry = _cache.get(key)
    if entry and time.time() - entry["ts"] < entry["ttl"]:
        return entry["data"]
    return None


def _set_cache(key: str, data: dict, ttl: int):
    _cache[key] = {"data": data, "ts": time.time(), "ttl": ttl}


async def _fetch(endpoint: str, params: dict | None = None) -> dict:
    """Make a request to CricAPI. Returns the full JSON response."""
    api_key = _get_api_key()
    if not api_key:
        return {"status": "failure", "reason": "No API key configured. Set CRICKET_API_KEY in backend/.env"}

    req_params = {"apikey": api_key, "offset": 0}
    if params:
        req_params.update(params)

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{CRICAPI_BASE}/{endpoint}", params=req_params)
        return resp.json()


def _is_pakistan_match(match: dict) -> bool:
    """Check if Pakistan is playing in this match."""
    # Check teams array: ["England", "Pakistan"]
    for t in match.get("teams", []) or []:
        if "pakistan" in str(t).lower():
            return True

    # Check teamInfo array: [{name, shortname, img}, ...]
    for ti in match.get("teamInfo", []) or []:
        if "pakistan" in (ti.get("name", "") or "").lower():
            return True
        if (ti.get("shortname", "") or "").upper() == "PAK":
            return True

    return False


def _classify_status(match: dict) -> str:
    """Classify match as live, completed, or upcoming from CricAPI fields."""
    started = match.get("matchStarted", False)
    ended = match.get("matchEnded", False)

    if ended:
        return "completed"
    if started and not ended:
        return "live"
    return "upcoming"


def _normalize_match(match: dict) -> dict:
    """Transform CricAPI match object into our frontend format."""
    status = _classify_status(match)
    teams = match.get("teams", []) or []
    team_info = match.get("teamInfo", []) or []

    team1 = teams[0] if len(teams) > 0 else "TBD"
    team2 = teams[1] if len(teams) > 1 else "TBD"

    # teamInfo may not be in same order as teams - map by name
    team1_img = ""
    team2_img = ""
    for ti in team_info:
        ti_name = (ti.get("name", "") or "").lower()
        # Match first word of team name
        if team1.lower().split()[0] in ti_name or ti_name in team1.lower():
            team1_img = ti.get("img", "")
        elif team2.lower().split()[0] in ti_name or ti_name in team2.lower():
            team2_img = ti.get("img", "")

    # If still not matched, assign by order
    if not team1_img and len(team_info) > 0:
        team1_img = team_info[0].get("img", "")
    if not team2_img and len(team_info) > 1:
        team2_img = team_info[1].get("img", "")

    # Scores: [{r, w, o, inning}, ...]
    raw_scores = match.get("score", []) or []
    scores = []
    for s in raw_scores:
        scores.append({
            "inning": s.get("inning", ""),
            "runs": s.get("r", 0),
            "wickets": s.get("w", 0),
            "overs": s.get("o", 0),
        })

    # Figure out which team is Pakistan
    pak_team = None
    opponent = None
    for t in [team1, team2]:
        if "pakistan" in t.lower():
            pak_team = t
        else:
            opponent = t
    if not pak_team:
        pak_team = team1
        opponent = team2

    return {
        "id": match.get("id", ""),
        "name": match.get("name", ""),
        "status": status,
        "match_type": (match.get("matchType", "") or "").upper(),
        "venue": match.get("venue", ""),
        "date": match.get("date", ""),
        "date_time_gmt": match.get("dateTimeGMT", ""),
        "team1": team1,
        "team2": team2,
        "team1_img": team1_img,
        "team2_img": team2_img,
        "pak_team": pak_team,
        "opponent": opponent,
        "scores": scores,
        "status_text": match.get("status", ""),
        "series": match.get("series_id", ""),
        "has_squad": match.get("hasSquad", False),
        # match_info fields (present only when fetched via match_info)
        "toss_winner": match.get("tossWinner", ""),
        "toss_choice": match.get("tossChoice", ""),
        "match_winner": match.get("matchWinner", ""),
    }


# === Public API ===

async def get_current_matches() -> dict:
    """Fetch live and recently completed matches, filtered to Pakistan."""
    cached = _get_cache("current_matches")
    if cached:
        return cached

    data = await _fetch("currentMatches")

    if data.get("status") != "success":
        return {"matches": [], "error": data.get("reason", "API error"), "source": "api"}

    all_matches = data.get("data", []) or []
    pak_matches = [_normalize_match(m) for m in all_matches if _is_pakistan_match(m)]

    result = {
        "matches": pak_matches,
        "total_pak": len(pak_matches),
        "total_all": len(all_matches),
        "api_hits": data.get("info", {}).get("hitsToday", "?"),
        "api_limit": data.get("info", {}).get("hitsLimit", "?"),
        "source": "api",
    }

    _set_cache("current_matches", result, CACHE_TTL["current_matches"])
    return result


async def get_all_matches() -> dict:
    """Fetch all matches (recent + upcoming), filtered to Pakistan."""
    cached = _get_cache("all_matches")
    if cached:
        return cached

    data = await _fetch("matches")

    if data.get("status") != "success":
        return {"matches": [], "error": data.get("reason", "API error"), "source": "api"}

    all_matches = data.get("data", []) or []
    pak_matches = [_normalize_match(m) for m in all_matches if _is_pakistan_match(m)]

    result = {
        "matches": pak_matches,
        "total_pak": len(pak_matches),
        "total_all": len(all_matches),
        "api_hits": data.get("info", {}).get("hitsToday", "?"),
        "api_limit": data.get("info", {}).get("hitsLimit", "?"),
        "source": "api",
    }

    _set_cache("all_matches", result, CACHE_TTL["all_matches"])
    return result


async def get_match_detail(match_id: str) -> dict:
    """
    Fetch detailed info for a single match using /v1/match_info.
    Returns scores per innings, toss info, winner, and team info.
    Note: full batting/bowling scorecard requires paid plan.
    """
    cache_key = f"match_info_{match_id}"
    cached = _get_cache(cache_key)
    if cached:
        return cached

    data = await _fetch("match_info", {"id": match_id})

    if data.get("status") != "success":
        return {"error": data.get("reason", "API error"), "source": "api"}

    match_data = data.get("data", {})
    result = _normalize_match(match_data)
    result["source"] = "api"

    _set_cache(cache_key, result, CACHE_TTL["match_info"])
    return result
