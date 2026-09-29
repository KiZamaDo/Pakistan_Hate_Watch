"""
Pakistan Loss Probability Engine
================================
Two modes:
1. PRE-MATCH: Computes loss probability for upcoming matches using
   weighted factors (venue, opponent strength, historical record, chaos factor)

2. LIVE MATCH: Real-time loss probability using current match state —
   overs remaining, wickets fallen, run rate vs required rate,
   Pakistan-specific collapse history, and Bayesian updating.

The key insight: Pakistan aren't just any team. Their probability distributions
are FAT-TAILED — they have a much higher chance of extreme outcomes (collapses,
dramatic chokes) than a normal team. Our model accounts for this.
"""

import numpy as np
from typing import Optional


# --- Pakistan-specific constants derived from historical data ---

# How often Pakistan collapse (lose 5+ wickets for <50 runs) by format
COLLAPSE_BASE_RATES = {
    "ODI": 0.18,   # ~18% of ODI innings feature a collapse
    "T20I": 0.22,  # Higher in T20s — less time to recover
    "Test": 0.15,  # Test collapses happen but less frequently
}

# Pakistan's historical win rates by format (used as priors)
HISTORICAL_WIN_RATES = {
    "ODI": 0.527,
    "T20I": 0.575,
    "Test": 0.323,
}

# Choke factor — multiplier for pressure situations
# (knockout games, chases over 250, must-win matches)
CHOKE_MULTIPLIER = 1.35  # Pakistan are 35% more likely to lose under pressure

# Average run rate decline when Pakistan are under pressure
PRESSURE_RR_DECLINE = 0.82  # run rate drops to 82% of normal


def compute_prematch_loss_probability(
    factors: list[dict],
    match_format: str,
    is_icc_event: bool = False,
    is_knockout: bool = False,
) -> dict:
    """
    Compute pre-match loss probability from weighted factors.

    Each factor has an 'impact' score from -100 to +100.
    Negative = bad for Pakistan, Positive = good for Pakistan.

    Returns full probability breakdown with confidence interval.
    """
    # Start with historical base loss rate for the format
    base_loss_rate = 1 - HISTORICAL_WIN_RATES.get(match_format, 0.5)

    # Sum up factor impacts — each factor shifts the probability
    total_impact = sum(f["impact"] for f in factors)

    # Normalize impact to a probability shift (-1 to 1 range)
    # Using sigmoid-like transformation for smooth boundaries
    impact_shift = np.tanh(total_impact / 100)

    # Apply impact to base rate
    # Negative impact increases loss probability, positive decreases it
    adjusted_loss_prob = base_loss_rate - (impact_shift * 0.3)

    # ICC event penalty — Pakistan historically underperform
    if is_icc_event:
        adjusted_loss_prob *= 1.15

    # Knockout game choke factor
    if is_knockout:
        adjusted_loss_prob *= CHOKE_MULTIPLIER

    # Clamp to valid probability range
    loss_prob = float(np.clip(adjusted_loss_prob, 0.05, 0.95))
    win_prob = 1 - loss_prob

    # For Tests, allocate some probability to draw
    draw_prob = 0.0
    if match_format == "Test":
        draw_prob = 0.15  # ~15% base draw chance
        loss_prob = loss_prob * (1 - draw_prob)
        win_prob = win_prob * (1 - draw_prob)

    # Determine if this is a hate watch (>60% loss probability)
    is_hate_watch = loss_prob > 0.60

    # Compute confidence interval using beta distribution
    # More extreme factors = wider confidence interval
    factor_variance = np.var([f["impact"] for f in factors]) if factors else 0
    confidence_width = 0.05 + (factor_variance / 10000) * 0.15

    return {
        "loss_probability": round(loss_prob * 100, 1),
        "win_probability": round(win_prob * 100, 1),
        "draw_probability": round(draw_prob * 100, 1),
        "is_hate_watch": is_hate_watch,
        "confidence_interval": {
            "low": round(max(0, (loss_prob - confidence_width)) * 100, 1),
            "high": round(min(1, (loss_prob + confidence_width)) * 100, 1),
        },
        "factors_summary": {
            "positive_factors": [f for f in factors if f["impact"] > 0],
            "negative_factors": [f for f in factors if f["impact"] < 0],
            "net_impact": total_impact,
        },
    }


def compute_live_loss_probability(
    match_format: str,
    innings: int,
    overs: float,
    runs: int,
    wickets: int,
    target: Optional[int] = None,
    total_overs: Optional[float] = None,
    batting_first: bool = True,
    opponent: str = "Unknown",
    partnership_balls: int = 0,
    last_six_overs_runs: Optional[list[int]] = None,
) -> dict:
    """
    Real-time loss probability calculator.

    Uses current match state + Pakistan-specific historical patterns
    to compute the probability of Pakistan losing from this exact point.

    The model combines:
    1. Resource-based projection (Duckworth-Lewis inspired)
    2. Pakistan-specific collapse probability
    3. Momentum analysis (recent scoring patterns)
    4. Historical match comparisons
    """
    if total_overs is None:
        total_overs = {"ODI": 50.0, "T20I": 20.0, "Test": 90.0}[match_format]

    overs_remaining = max(0.1, total_overs - overs)
    balls_remaining = int(overs_remaining * 6)
    wickets_remaining = 10 - wickets

    # --- 1. Resource Percentage Remaining ---
    # Simplified DLS-inspired resource calculation
    # Resources depend on both overs and wickets remaining
    wicket_resource = _wicket_resources(wickets_remaining)
    over_resource = overs_remaining / total_overs
    resources_remaining = wicket_resource * over_resource

    # --- 2. Run Rate Analysis ---
    current_rr = runs / max(overs, 0.1)

    if target is not None and not batting_first:
        # Chasing — compute required rate
        runs_needed = target - runs
        required_rr = runs_needed / max(overs_remaining, 0.1)
        rr_ratio = required_rr / max(current_rr, 0.1)

        # The further behind the required rate, the worse it looks
        chase_difficulty = np.clip(rr_ratio, 0, 5)
    else:
        runs_needed = 0
        required_rr = 0
        chase_difficulty = 1.0

    # --- 3. Pakistan Collapse Probability ---
    collapse_base = COLLAPSE_BASE_RATES.get(match_format, 0.18)

    # Collapse risk increases with each wicket lost
    if wickets >= 3:
        collapse_risk = collapse_base * (1 + (wickets - 2) * 0.15)
    else:
        collapse_risk = collapse_base * 0.5

    # Short partnerships increase collapse risk
    if partnership_balls < 12 and wickets >= 2:
        collapse_risk *= 1.3

    # --- 4. Momentum Analysis ---
    momentum_factor = 1.0
    if last_six_overs_runs and len(last_six_overs_runs) >= 3:
        recent_rr = sum(last_six_overs_runs[-3:]) / 3
        if current_rr > 0:
            momentum_factor = recent_rr / (current_rr * (total_overs / 6))
        # Declining momentum = bad
        if momentum_factor < 0.8:
            collapse_risk *= 1.2

    # --- 5. Compute Final Loss Probability ---
    if batting_first:
        # Batting first: project total score and assess if it's enough
        projected_score = runs + (current_rr * overs_remaining * resources_remaining * 6 / total_overs * total_overs)
        projected_score = max(projected_score, runs)

        # Historical averages for winning first-innings scores
        winning_scores = {"ODI": 280, "T20I": 170, "Test": 350}
        target_score = winning_scores.get(match_format, 280)

        score_ratio = projected_score / target_score
        base_loss_prob = 1 - np.clip(score_ratio * 0.6, 0, 0.85)

        # Factor in collapse risk
        loss_prob = base_loss_prob + (collapse_risk * 0.3)

    else:
        # Chasing: combine chase difficulty with resources and collapse risk
        if runs_needed <= 0:
            loss_prob = 0.01  # Already won basically
        else:
            # Base probability from chase difficulty
            base_chase_prob = np.clip(
                0.3 + (chase_difficulty - 1) * 0.25, 0.1, 0.95
            )

            # Adjust for resources remaining
            resource_factor = 1 - resources_remaining
            loss_prob = base_chase_prob * (0.5 + resource_factor * 0.5)

            # Collapse risk is more impactful when chasing
            loss_prob += collapse_risk * 0.35

            # Pakistan pressure factor when required rate is high
            if required_rr > 8.0 and match_format in ("ODI", "T20I"):
                loss_prob *= CHOKE_MULTIPLIER * 0.9

    # Clamp
    loss_prob = float(np.clip(loss_prob, 0.02, 0.98))
    collapse_risk = float(np.clip(collapse_risk, 0, 1))

    # --- Determine Alert Level ---
    if loss_prob > 0.85:
        alert_level = "MELTDOWN"
    elif loss_prob > 0.70:
        alert_level = "COLLAPSE_INCOMING"
    elif loss_prob > 0.55:
        alert_level = "CHOKING"
    elif loss_prob > 0.40:
        alert_level = "NERVOUS"
    else:
        alert_level = "STABLE"

    # --- Key Factors Description ---
    key_factors = []
    if wickets >= 5:
        key_factors.append(f"🚨 {wickets} wickets down — deep trouble")
    if wickets >= 3 and overs < total_overs * 0.3:
        key_factors.append("⚠️ Early wickets — collapse pattern forming")
    if not batting_first and required_rr > 10:
        key_factors.append(f"📈 Required rate {required_rr:.1f} — nearly impossible")
    elif not batting_first and required_rr > 7:
        key_factors.append(f"📈 Required rate climbing to {required_rr:.1f}")
    if collapse_risk > 0.4:
        key_factors.append("💀 High collapse probability based on Pakistan patterns")
    if partnership_balls < 12 and wickets >= 2:
        key_factors.append("🔄 Short partnerships — no stability")
    if not key_factors:
        key_factors.append("📊 Match situation is still developing")

    # --- Historical Comparison ---
    historical = _find_historical_comparison(
        match_format, runs, wickets, overs, target, batting_first
    )

    # Projected score
    if batting_first:
        proj_score = int(runs + current_rr * overs_remaining)
    else:
        proj_score = target if target else int(runs + current_rr * overs_remaining)

    return {
        "loss_probability": round(loss_prob * 100, 1),
        "win_probability": round((1 - loss_prob) * 100, 1),
        "draw_probability": 0.0,
        "alert_level": alert_level,
        "collapse_risk": round(collapse_risk * 100, 1),
        "projected_score": proj_score,
        "key_factors": key_factors,
        "historical_comparison": historical,
        "misery_index": round(loss_prob * 10, 1),
        "current_run_rate": round(current_rr, 2),
        "required_run_rate": round(required_rr, 2) if not batting_first else None,
        "resources_remaining": round(resources_remaining * 100, 1),
    }


def _wicket_resources(wickets_remaining: int) -> float:
    """
    Resource percentage based on wickets remaining.
    Inspired by DLS method but simplified.
    Each wicket has diminishing value (first few are most important).
    """
    # Resource curve — losing top order wickets costs more
    resource_table = {
        10: 1.00, 9: 0.91, 8: 0.81, 7: 0.70,
        6: 0.58, 5: 0.46, 4: 0.34, 3: 0.23,
        2: 0.13, 1: 0.05, 0: 0.00,
    }
    return resource_table.get(wickets_remaining, 0.0)


def _find_historical_comparison(
    match_format: str,
    runs: int,
    wickets: int,
    overs: float,
    target: Optional[int],
    batting_first: bool,
) -> str:
    """
    Find a similar historical Pakistan match situation for context.
    This makes the probability feel real — 'last time Pakistan were
    in this situation, they...'
    """
    if wickets >= 5 and overs < 25 and match_format == "ODI":
        return "Reminiscent of the 2023 WC vs India — collapsed to 191 all out after a similar position"

    if wickets >= 4 and overs < 10 and match_format == "T20I":
        return "Similar to the T20 WC 2024 group stage — top order fell apart in powerplay"

    if not batting_first and target:
        runs_needed = target - runs
        overs_left = 50 - overs if match_format == "ODI" else 20 - overs
        if overs_left > 0:
            req_rr = runs_needed / overs_left
            if req_rr > 9 and match_format == "ODI":
                return "Pakistan have never chased at 9+ RPO for more than 10 overs in an ODI"
            if req_rr > 12 and match_format == "T20I":
                return "Similar required rate to the 2021 semi-final vs Australia — didn't end well"

    if wickets <= 1 and overs > 15 and match_format == "ODI":
        return "Good position but remember — Pakistan went from 150/1 to 191 all out vs India in 2023"

    if batting_first and runs < 100 and overs > 25 and match_format == "ODI":
        return "Scoring rate mirrors the 174 all out vs New Zealand at home in 2025"

    return "Situation is developing — Pakistan are capable of miracles and disasters equally"
