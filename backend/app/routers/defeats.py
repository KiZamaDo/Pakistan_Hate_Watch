"""
Defeats Router — Recent defeats and tournament record
"""

from fastapi import APIRouter, Query
from typing import Optional

from app.data.defeats import RECENT_DEFEATS, TOURNAMENT_RECORD

router = APIRouter()


@router.get("/recent")
def get_recent_defeats(
    limit: int = Query(10, ge=1, le=50),
    category: Optional[str] = Query(None, description="Filter: humiliating, embarrassing, expected"),
    format: Optional[str] = Query(None, description="Filter: Test, ODI, T20I"),
):
    results = RECENT_DEFEATS
    if category:
        results = [d for d in results if d["category"] == category]
    if format:
        results = [d for d in results if d["format"] == format]
    return {"total": len(results), "defeats": results[:limit]}


@router.get("/tournament-record")
def get_tournament_record():
    return {
        "total": len(TOURNAMENT_RECORD),
        "trophies_won": 0,
        "tournaments": TOURNAMENT_RECORD,
    }


@router.get("/worst")
def get_worst_defeats(limit: int = Query(5, ge=1, le=15)):
    sorted_defeats = sorted(RECENT_DEFEATS, key=lambda d: d["misery"], reverse=True)
    return {"total": len(sorted_defeats), "worst_defeats": sorted_defeats[:limit]}
