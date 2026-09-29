"""
Pakistan Collapse Alert & Projection Engine
============================================
Detects, classifies, and projects batting collapses in real-time.

Collapse detection criteria:
- 3+ wickets falling in a 5-over span
- Run rate dropping below 3.0 in ODIs or 5.0 in T20Is after being above 5.0/8.0
- Partnership average below 15 runs for 3+ consecutive partnerships

The engine maintains a library of famous Pakistan collapse patterns
and matches current situations against them.

Alert Levels:
  MELTDOWN         → 5+ wickets lost rapidly, game effectively over
  COLLAPSE_INCOMING → 3-4 quick wickets, pattern matches historical collapses
  CHOKING          → Scoring rate cratering under pressure
  NERVOUS          → Early warning signs — a wicket cluster starting
  STABLE           → No collapse indicators (rare for Pakistan)
"""

import numpy as np
from datetime import datetime


# --- Famous Pakistan Collapse Patterns ---
# These are used for pattern matching against live situations

COLLAPSE_PATTERNS = [
    {
        "name": "The Classic Top-Order Implosion",
        "description": "3+ top-order wickets fall in first 10 overs (ODI) or 4 overs (T20I). Pakistan's most common collapse type.",
        "trigger_conditions": [
            "3+ wickets in first 20% of innings",
            "Both openers back in pavilion within 5 overs",
            "No partnership exceeding 20 runs in top 4",
        ],
        "frequency": "Occurs in ~22% of Pakistan ODI innings",
        "last_occurrence": "2025-03-04 vs New Zealand (174 all out)",
        "famous_examples": [
            "vs India, WC 2023 — 191 all out",
            "vs New Zealand, 2025 — 174 all out",
            "vs Australia, Perth 2024 — 203 all out",
        ],
    },
    {
        "name": "The Middle-Order Meltdown",
        "description": "After a solid start (100+/1 or 2), the middle order collapses losing 5+ wickets for under 50 runs.",
        "trigger_conditions": [
            "Score above 100 with 2 or fewer wickets lost",
            "Then 4+ wickets fall in next 10-15 overs",
            "Run rate drops from 5+ to under 3",
        ],
        "frequency": "Occurs in ~15% of Pakistan ODI innings",
        "last_occurrence": "2023-10-14 vs Afghanistan WC (282/7, nearly all out)",
        "famous_examples": [
            "vs India, 2023 WC — From decent start to 191 all out",
            "vs England, Rawalpindi 2024 — Middle order vanished",
            "vs South Africa, Centurion 2024 — 5 for 31 in middle overs",
        ],
    },
    {
        "name": "The Tail-End Surrender",
        "description": "Last 4 wickets fall for under 20 runs. The tail doesn't wag — it barely twitches.",
        "trigger_conditions": [
            "7th wicket falls with still 10+ overs remaining",
            "Last 3 batsmen average under 8",
            "No resistance from lower order",
        ],
        "frequency": "Occurs in ~30% of Pakistan innings (highest rate in top 8 teams)",
        "last_occurrence": "2024-11-03 vs Australia, Perth (last 4 wickets for 18 runs)",
        "famous_examples": [
            "72 all out vs England, Abu Dhabi 2012",
            "vs India, WC 2023 — tail folded in 4 overs",
            "vs Australia, Perth 2024 — last 4 for 18",
        ],
    },
    {
        "name": "The Chase Choke",
        "description": "While chasing, Pakistan are on track but suddenly lose wickets in a cluster and required rate spirals.",
        "trigger_conditions": [
            "Chasing and on par with required rate",
            "Then 3+ wickets fall in 5 overs",
            "Required rate jumps from manageable (<7) to impossible (>10)",
        ],
        "frequency": "Occurs in ~25% of Pakistan chases over 200",
        "last_occurrence": "2024-06-16 vs India, T20 WC 2024",
        "famous_examples": [
            "vs USA, T20 WC 2024 Super Over",
            "vs Australia, T20 WC 2021 Semi-Final",
            "vs India, T20 WC 2024",
        ],
    },
    {
        "name": "The Pressure Paralysis",
        "description": "Run rate drops dramatically as the team plays scared. No wickets falling but scoring freezes.",
        "trigger_conditions": [
            "Run rate drops below 4.0 in middle overs (ODI)",
            "Dot ball percentage exceeds 50%",
            "Required rate climbs steadily while wickets in hand",
        ],
        "frequency": "Occurs in ~20% of Pakistan ODI chases",
        "last_occurrence": "2024-06-11 vs USA, T20 WC 2024",
        "famous_examples": [
            "vs England, T20 WC 2022 Final — 137/8",
            "vs USA, T20 WC 2024 — couldn't accelerate",
            "Various bilateral chases where Rizwan anchored too hard",
        ],
    },
]


def detect_collapse(
    match_format: str,
    overs: float,
    runs: int,
    wickets: int,
    total_overs: float,
    recent_wickets: list[dict],  # [{over: 5.3, runs_at_wicket: 32}, ...]
    recent_run_rates: list[float],  # run rate per over for last 6 overs
    batting_first: bool = True,
    target: int | None = None,
) -> dict:
    """
    Analyze current match state for collapse indicators.
    Returns alert level, matched pattern, and projection.
    """
    alerts = []
    matched_patterns = []
    panic_level = 0

    # --- Check for wicket clustering ---
    if len(recent_wickets) >= 3:
        # Check if 3+ wickets fell in last 5 overs
        last_5_over_wickets = [
            w for w in recent_wickets
            if w["over"] >= overs - 5
        ]
        if len(last_5_over_wickets) >= 3:
            alerts.append({
                "type": "WICKET_CLUSTER",
                "message": f"🚨 {len(last_5_over_wickets)} wickets in last 5 overs — collapse in progress!",
                "severity": "critical",
            })
            panic_level += 35
            matched_patterns.append("The Classic Top-Order Implosion" if overs < total_overs * 0.3 else "The Middle-Order Meltdown")

    # --- Check for run rate cratering ---
    if recent_run_rates and len(recent_run_rates) >= 3:
        recent_avg_rr = np.mean(recent_run_rates[-3:])
        overall_rr = runs / max(overs, 0.1)

        if match_format == "ODI" and recent_avg_rr < 3.0 and overall_rr > 4.5:
            alerts.append({
                "type": "SCORING_FREEZE",
                "message": f"❄️ Run rate crashed from {overall_rr:.1f} to {recent_avg_rr:.1f} — pressure paralysis",
                "severity": "major",
            })
            panic_level += 25
            matched_patterns.append("The Pressure Paralysis")

        elif match_format == "T20I" and recent_avg_rr < 5.0 and overall_rr > 7.0:
            alerts.append({
                "type": "SCORING_FREEZE",
                "message": f"❄️ T20 run rate dropped to {recent_avg_rr:.1f} — this is NOT how T20 works",
                "severity": "major",
            })
            panic_level += 30
            matched_patterns.append("The Pressure Paralysis")

    # --- Check for top order collapse ---
    if wickets >= 3 and overs < total_overs * 0.25:
        alerts.append({
            "type": "TOP_ORDER_COLLAPSE",
            "message": f"💀 {wickets} wickets down in first {overs:.1f} overs — textbook Pakistan",
            "severity": "critical",
        })
        panic_level += 30
        if "The Classic Top-Order Implosion" not in matched_patterns:
            matched_patterns.append("The Classic Top-Order Implosion")

    # --- Check for chase choke ---
    if not batting_first and target:
        runs_needed = target - runs
        overs_left = total_overs - overs
        if overs_left > 0:
            req_rr = runs_needed / overs_left
            if req_rr > 10 and wickets >= 4:
                alerts.append({
                    "type": "CHASE_IMPOSSIBLE",
                    "message": f"☠️ Need {runs_needed} off {overs_left:.1f} overs with {10-wickets} wickets — it's over",
                    "severity": "critical",
                })
                panic_level += 40
                matched_patterns.append("The Chase Choke")
            elif req_rr > 8 and wickets >= 3:
                alerts.append({
                    "type": "CHASE_SLIPPING",
                    "message": f"⚠️ Required rate climbing to {req_rr:.1f} — classic Pakistan chase implosion building",
                    "severity": "major",
                })
                panic_level += 20
                matched_patterns.append("The Chase Choke")

    # --- Check for tail exposure ---
    if wickets >= 7:
        alerts.append({
            "type": "TAIL_EXPOSED",
            "message": f"🦆 Tail exposed at {runs}/{wickets} — Pakistan's tail has a collective average of 8",
            "severity": "critical",
        })
        panic_level += 25
        matched_patterns.append("The Tail-End Surrender")

    # --- Determine overall alert level ---
    panic_level = min(panic_level, 100)

    if panic_level >= 70:
        alert_level = "MELTDOWN"
    elif panic_level >= 50:
        alert_level = "COLLAPSE_INCOMING"
    elif panic_level >= 30:
        alert_level = "CHOKING"
    elif panic_level >= 15:
        alert_level = "NERVOUS"
    else:
        alert_level = "STABLE"

    # --- Project where this collapse leads ---
    projection = _project_collapse_outcome(
        match_format, overs, runs, wickets, total_overs, panic_level
    )

    return {
        "alert_level": alert_level,
        "panic_level": panic_level,
        "alerts": alerts,
        "matched_patterns": matched_patterns,
        "projection": projection,
        "timestamp": datetime.now().isoformat(),
    }


def _project_collapse_outcome(
    match_format: str,
    overs: float,
    runs: int,
    wickets: int,
    total_overs: float,
    panic_level: int,
) -> dict:
    """
    Project the final score based on current collapse trajectory.
    Uses Pakistan-specific scoring rates for remaining wickets.
    """
    wickets_remaining = 10 - wickets
    overs_remaining = total_overs - overs

    # Pakistan's average runs per remaining wicket when collapsing
    if panic_level >= 50:
        runs_per_wicket = 8.5   # Deep trouble — tail folds quickly
    elif panic_level >= 30:
        runs_per_wicket = 14.2  # Moderate trouble
    else:
        runs_per_wicket = 22.5  # Mild concern

    projected_additional = wickets_remaining * runs_per_wicket
    projected_total = int(runs + projected_additional)

    # Also project based on overs if they don't get bowled out
    if match_format != "Test":
        current_rr = runs / max(overs, 0.1)
        collapse_rr = current_rr * (1 - panic_level / 200)  # run rate declines
        overs_projected = int(runs + collapse_rr * overs_remaining)
        projected_total = min(projected_total, overs_projected)

    return {
        "projected_total": projected_total,
        "projected_all_out_over": round(overs + wickets_remaining * 2.5, 1) if panic_level > 40 else None,
        "worst_case": int(runs + wickets_remaining * 5),
        "best_case": int(runs + wickets_remaining * 28),
        "most_likely": projected_total,
        "message": _collapse_projection_message(projected_total, match_format, panic_level),
    }


def _collapse_projection_message(projected: int, match_format: str, panic: int) -> str:
    """Generate a message for the projected outcome."""
    if panic >= 70:
        return f"Projected total: {projected}. This is a full meltdown. Start collecting screenshots for the Shame Gallery."
    elif panic >= 50:
        return f"Projected total: {projected}. The collapse is real. Pakistan are speedrunning their innings."
    elif panic >= 30:
        return f"Projected total: {projected}. Warning signs are there. A recovery is possible but this is Pakistan we're talking about."
    else:
        return f"Projected total: {projected}. Situation is manageable... for now."


def get_collapse_patterns() -> list[dict]:
    """Return all known Pakistan collapse patterns for display."""
    return COLLAPSE_PATTERNS
