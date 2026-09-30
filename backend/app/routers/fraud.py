"""
Fraud Watch Router - Player performance fraud detection
"""

from fastapi import APIRouter, Query
from typing import Optional

from app.data.players import PLAYER_PROFILES
from app.engines.fraud_engine import compute_fraud_score, get_fraud_rating_label

router = APIRouter()


@router.get("/players")
def get_all_fraud_profiles(
    rating: Optional[str] = Query(None, description="Filter: certified-fraud, suspect, underperformer, inconsistent, redeemable"),
    sort_by: str = Query("overall_rating", description="Sort by: overall_rating, fraud_rating, name"),
):
    """
    Get all player fraud profiles with computed fraud scores.
    Each player runs through the Fraud Detection Engine for real-time scoring.
    """
    results = []
    for player in PLAYER_PROFILES:
        # Run through fraud engine
        fraud_analysis = compute_fraud_score(player)

        profile = {
            **player,
            "computed_fraud_rating": fraud_analysis["fraud_rating"],
            "computed_overall_score": fraud_analysis["overall_score"],
            "fraud_components": fraud_analysis["components"],
            "fraud_analysis": fraud_analysis["analysis"],
            "rating_display": get_fraud_rating_label(fraud_analysis["fraud_rating"]),
        }
        results.append(profile)

    if rating:
        results = [p for p in results if p["computed_fraud_rating"] == rating]

    # Sort
    if sort_by == "overall_rating":
        results.sort(key=lambda p: p["computed_overall_score"])
    elif sort_by == "name":
        results.sort(key=lambda p: p["name"])

    return {
        "total": len(results),
        "players": results,
        "rating_summary": {
            "certified_frauds": sum(1 for p in results if p["computed_fraud_rating"] == "certified-fraud"),
            "suspects": sum(1 for p in results if p["computed_fraud_rating"] == "suspect"),
            "underperformers": sum(1 for p in results if p["computed_fraud_rating"] == "underperformer"),
            "inconsistent": sum(1 for p in results if p["computed_fraud_rating"] == "inconsistent"),
            "redeemable": sum(1 for p in results if p["computed_fraud_rating"] == "redeemable"),
        },
    }


@router.get("/player/{player_id}")
def get_player_fraud_profile(player_id: str):
    """Get detailed fraud profile for a specific player."""
    player = next((p for p in PLAYER_PROFILES if p["id"] == player_id), None)
    if not player:
        return {"error": "Player not found", "message": "Maybe they've been dropped again?"}

    fraud_analysis = compute_fraud_score(player)

    return {
        **player,
        "computed_fraud_rating": fraud_analysis["fraud_rating"],
        "computed_overall_score": fraud_analysis["overall_score"],
        "fraud_components": fraud_analysis["components"],
        "fraud_analysis": fraud_analysis["analysis"],
        "rating_display": get_fraud_rating_label(fraud_analysis["fraud_rating"]),
    }
