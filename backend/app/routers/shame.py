"""
Shame Gallery Router — YouTube videos of Pakistan's finest losses
"""

from fastapi import APIRouter, Query
from typing import Optional

from app.data.shame_gallery import SHAME_VIDEOS

router = APIRouter()


@router.get("/videos")
def get_shame_videos(
    category: Optional[str] = Query(None, description="Filter: collapse, choke, upset-loss, bowling-disaster, fielding-horror, captaincy-blunder, tournament-exit, all-time-low"),
    sort_by: str = Query("shame_rating", description="Sort by: shame_rating, date, view_count"),
    limit: int = Query(20, ge=1, le=50),
):
    """
    Get the Shame Gallery — curated YouTube videos of Pakistan's most memorable defeats.
    """
    results = SHAME_VIDEOS

    if category:
        results = [v for v in results if v["category"] == category]

    if sort_by == "shame_rating":
        results = sorted(results, key=lambda v: v["shame_rating"], reverse=True)
    elif sort_by == "date":
        results = sorted(results, key=lambda v: v["date"], reverse=True)

    return {
        "total": len(results),
        "videos": results[:limit],
        "categories": list(set(v["category"] for v in SHAME_VIDEOS)),
        "hall_of_shame_top3": sorted(SHAME_VIDEOS, key=lambda v: v["shame_rating"], reverse=True)[:3],
    }


@router.get("/video/{video_id}")
def get_shame_video(video_id: str):
    """Get a specific shame video by ID."""
    video = next((v for v in SHAME_VIDEOS if v["id"] == video_id), None)
    if not video:
        return {"error": "Video not found", "message": "Even our shame has limits (just kidding, it doesn't)"}
    return video
