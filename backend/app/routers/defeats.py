"""
Defeats Router — Recent defeats and tournament exits
"""

from fastapi import APIRouter, Query
from typing import Optional

from app.data.defeats import RECENT_DEFEATS, TOURNAMENT_EXITS

router = APIRouter()


@router.get("/recent")
def get_recent_defeats(
    limit: int = Query(10, ge=1, le=50),
    severity: Optional[str] = Query(None, description="Filter: humiliating, painful, embarrassing, expected"),
    format: Optional[str] = Query(None, description="Filter: Test, ODI, T20I"),
):
    """Get recent Pakistan defeats, optionally filtered."""
    results = RECENT_DEFEATS

    if severity:
        results = [d for d in results if d["severity"] == severity]
    if format:
        results = [d for d in results if d["format"] == format]

    return {
        "total": len(results),
        "defeats": results[:limit],
    }


@router.get("/tournament-exits")
def get_tournament_exits(limit: int = Query(10, ge=1, le=20)):
    """Get Pakistan's tournament exit history — a catalogue of pain."""
    return {
        "total": len(TOURNAMENT_EXITS),
        "exits": TOURNAMENT_EXITS[:limit],
    }


@router.get("/worst")
def get_worst_defeats(limit: int = Query(5, ge=1, le=15)):
    """Get the worst defeats by misery rating."""
    sorted_defeats = sorted(RECENT_DEFEATS, key=lambda d: d["misery_rating"], reverse=True)
    return {
        "total": len(sorted_defeats),
        "worst_defeats": sorted_defeats[:limit],
    }
