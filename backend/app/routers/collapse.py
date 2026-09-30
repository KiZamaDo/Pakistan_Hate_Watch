"""
Collapse Alert Router - Collapse detection and projection
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

from app.engines.collapse_engine import detect_collapse, get_collapse_patterns

router = APIRouter()


class CollapseInput(BaseModel):
    """Input for collapse detection."""
    match_format: str = Field(..., description="ODI, T20I, or Test")
    overs: float = Field(..., ge=0)
    runs: int = Field(..., ge=0)
    wickets: int = Field(..., ge=0, le=10)
    total_overs: float = Field(50.0)
    recent_wickets: list[dict] = Field(
        default=[],
        description="List of {over, runs_at_wicket} for recent wickets"
    )
    recent_run_rates: list[float] = Field(
        default=[],
        description="Run rate per over for the last several overs"
    )
    batting_first: bool = Field(True)
    target: Optional[int] = Field(None)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "match_format": "ODI",
                    "overs": 18.2,
                    "runs": 67,
                    "wickets": 5,
                    "total_overs": 50.0,
                    "recent_wickets": [
                        {"over": 14.1, "runs_at_wicket": 52},
                        {"over": 15.5, "runs_at_wicket": 55},
                        {"over": 17.3, "runs_at_wicket": 61},
                    ],
                    "recent_run_rates": [4.2, 3.1, 1.5, 2.8, 3.0, 2.2],
                    "batting_first": True,
                }
            ]
        }
    }


@router.post("/detect")
def detect_collapse_alert(collapse_input: CollapseInput):
    """
    Analyze current match state for collapse indicators.
    Returns alert level, matched patterns, and projected outcome.
    """
    result = detect_collapse(
        match_format=collapse_input.match_format,
        overs=collapse_input.overs,
        runs=collapse_input.runs,
        wickets=collapse_input.wickets,
        total_overs=collapse_input.total_overs,
        recent_wickets=collapse_input.recent_wickets,
        recent_run_rates=collapse_input.recent_run_rates,
        batting_first=collapse_input.batting_first,
        target=collapse_input.target,
    )
    return result


@router.get("/patterns")
def get_pakistan_collapse_patterns():
    """
    Get all known Pakistan collapse patterns with historical examples.
    Useful for the 'Know Your Collapses' section of the dashboard.
    """
    patterns = get_collapse_patterns()
    return {
        "total_patterns": len(patterns),
        "patterns": patterns,
        "summary": "Pakistan have 5 distinct collapse patterns, each more painful than the last.",
    }
