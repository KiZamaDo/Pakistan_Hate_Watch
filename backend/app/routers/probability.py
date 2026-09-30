"""
Probability Router - Real-time loss probability calculator
The crown jewel of the Hate Watch.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

from app.engines.probability_engine import compute_live_loss_probability

router = APIRouter()


class LiveMatchInput(BaseModel):
    """Input for the real-time probability calculator."""
    match_format: str = Field(..., description="ODI, T20I, or Test")
    innings: int = Field(1, ge=1, le=4)
    overs: float = Field(..., ge=0, description="Current overs (e.g. 15.3)")
    runs: int = Field(..., ge=0, description="Current runs scored")
    wickets: int = Field(..., ge=0, le=10, description="Wickets fallen")
    target: Optional[int] = Field(None, description="Target score (if chasing)")
    total_overs: Optional[float] = Field(None, description="Total overs in innings")
    batting_first: bool = Field(True, description="Is Pakistan batting first?")
    opponent: str = Field("Unknown", description="Opponent team name")
    partnership_balls: int = Field(0, ge=0, description="Balls in current partnership")
    last_six_overs_runs: Optional[list[int]] = Field(None, description="Runs scored in each of last 6 overs")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "match_format": "ODI",
                    "innings": 1,
                    "overs": 25.3,
                    "runs": 112,
                    "wickets": 4,
                    "batting_first": True,
                    "opponent": "India",
                    "partnership_balls": 8,
                    "last_six_overs_runs": [4, 3, 6, 2, 5, 3],
                },
                {
                    "match_format": "T20I",
                    "innings": 2,
                    "overs": 12.0,
                    "runs": 78,
                    "wickets": 5,
                    "target": 186,
                    "batting_first": False,
                    "opponent": "Australia",
                    "partnership_balls": 3,
                    "last_six_overs_runs": [6, 4, 8, 5, 3, 7],
                },
            ]
        }
    }


@router.post("/calculate")
def calculate_live_probability(match_input: LiveMatchInput):
    """
    Calculate real-time loss probability from current match state.

    Send the current match situation and get back:
    - Loss/win probability
    - Alert level (MELTDOWN → STABLE)
    - Collapse risk percentage
    - Projected score
    - Key factors affecting the probability
    - Historical comparison to similar Pakistan situations
    """
    result = compute_live_loss_probability(
        match_format=match_input.match_format,
        innings=match_input.innings,
        overs=match_input.overs,
        runs=match_input.runs,
        wickets=match_input.wickets,
        target=match_input.target,
        total_overs=match_input.total_overs,
        batting_first=match_input.batting_first,
        opponent=match_input.opponent,
        partnership_balls=match_input.partnership_balls,
        last_six_overs_runs=match_input.last_six_overs_runs,
    )

    return result
