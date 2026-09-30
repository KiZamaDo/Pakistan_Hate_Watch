"""
Scorecard Router - Full batting/bowling tables via Cricbuzz scraper
===================================================================
Cricbuzz match IDs are different from CricAPI IDs, so we:
1. Provide a search endpoint to find a Cricbuzz match by team names
2. Provide a scorecard endpoint that takes a Cricbuzz match ID
"""

from fastapi import APIRouter
from app.services.cricbuzz_scraper import get_matches, get_scorecard

router = APIRouter()


@router.get("/cricbuzz/matches")
async def cricbuzz_matches():
    """
    Get Pakistan matches from Cricbuzz (live, recent, upcoming).
    These have Cricbuzz match IDs which can be used for scorecards.
    """
    data = await get_matches()
    return data


@router.get("/cricbuzz/{match_id}")
async def cricbuzz_scorecard(match_id: str):
    """
    Get full scorecard from Cricbuzz for a given Cricbuzz match ID.
    Returns batting + bowling tables with player names, runs, balls, SR, etc.
    """
    data = await get_scorecard(match_id)
    return data
