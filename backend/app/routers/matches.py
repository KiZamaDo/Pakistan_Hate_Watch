"""
Matches Router — Real-time match data from CricAPI
===================================================
Endpoints:
  GET /live         — current/live Pakistan matches
  GET /all          — all Pakistan matches (filterable by status)
  GET /{id}/detail  — single match detail with scores + our analysis overlay
"""

from fastapi import APIRouter, Query
from typing import Optional

from app.services.cricket_api import get_current_matches, get_all_matches, get_match_detail
from app.engines.probability_engine import compute_live_loss_probability
from app.engines.fraud_engine import compute_fraud_score, get_fraud_rating_label
from app.data.players import PLAYER_PROFILES

router = APIRouter()


@router.get("/live")
async def live_matches():
    """Get current/live Pakistan matches from CricAPI."""
    return await get_current_matches()


@router.get("/all")
async def all_matches(
    status: Optional[str] = Query(None, description="Filter: live, completed, upcoming"),
):
    """Get all Pakistan matches, optionally filtered by status."""
    data = await get_all_matches()
    matches = data.get("matches", [])

    if status:
        matches = [m for m in matches if m["status"] == status]

    return {
        "matches": matches,
        "total": len(matches),
        "source": data.get("source", "api"),
        "api_hits": data.get("api_hits"),
        "api_limit": data.get("api_limit"),
    }


@router.get("/{match_id}/detail")
async def match_detail(match_id: str):
    """
    Single match detail with our analysis overlaid.

    Returns:
    - Match info from CricAPI (scores per innings, toss, venue, result)
    - Our loss probability calculation for Pakistan's current position
    - Fraud alerts for any Pakistan players we track
    """
    match = await get_match_detail(match_id)

    if "error" in match:
        return match

    # --- Compute loss probability ONLY for live matches ---
    loss_analysis = None
    if match.get("status") == "live":
        loss_analysis = _compute_loss_from_scores(match)

    # --- Fraud alerts for players in our database ---
    fraud_alerts = _get_fraud_alerts_for_match(match)

    return {
        **match,
        "loss_analysis": loss_analysis,
        "fraud_alerts": fraud_alerts,
    }


def _compute_loss_from_scores(match: dict) -> dict | None:
    """Compute loss probability from the match's innings scores."""
    scores = match.get("scores", [])
    if not scores:
        return None

    # Find Pakistan's latest innings
    pak_innings = None
    opp_innings = None
    pak_innings_idx = -1

    for i, s in enumerate(scores):
        inning_name = (s.get("inning", "") or "").lower()
        if "pakistan" in inning_name:
            pak_innings = s
            pak_innings_idx = i
        else:
            opp_innings = s

    if not pak_innings:
        return None

    runs = pak_innings.get("runs", 0)
    wickets = pak_innings.get("wickets", 0)
    overs = float(pak_innings.get("overs", 0) or 0)

    # Determine format
    match_type = match.get("match_type", "ODI")
    format_map = {"T20": "T20I", "T20I": "T20I", "ODI": "ODI", "TEST": "Test"}
    fmt = format_map.get(match_type.upper(), "ODI")

    # Determine if chasing
    batting_first = pak_innings_idx == 0
    target = None
    if not batting_first and opp_innings:
        target = opp_innings.get("runs", 0) + 1

    try:
        return compute_live_loss_probability(
            match_format=fmt,
            innings=pak_innings_idx + 1,
            overs=overs,
            runs=runs,
            wickets=wickets,
            target=target,
            batting_first=batting_first,
            opponent=match.get("opponent", "Unknown"),
            partnership_balls=0,
        )
    except Exception:
        return None


def _get_fraud_alerts_for_match(match: dict) -> list:
    """Match player names from our fraud profiles against the match teams."""
    alerts = []
    pak_team = (match.get("pak_team", "") or "").lower()

    # We can't get individual player names from match_info on free tier,
    # so we return alerts for all tracked players when Pakistan is playing
    if "pakistan" in pak_team:
        for player in PLAYER_PROFILES:
            fraud = compute_fraud_score(player)
            alerts.append({
                "player_name": player["name"],
                "role": player["role"],
                "fraud_rating": fraud["fraud_rating"],
                "fraud_score": fraud["overall_score"],
                "rating_display": get_fraud_rating_label(fraud["fraud_rating"]),
                "analysis": fraud["analysis"],
                "red_flags": player.get("red_flags", [])[:2],
                "verdict": player.get("verdict_summary", ""),
            })

    return alerts
