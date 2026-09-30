"""
Pakistan Loss Probability Engine
================================
PRE-MATCH MODE (new):
  Calculates probability of Pakistan losing an upcoming match using:
  1. Head-to-Head record vs opponent (20%)
  2. Opponent ICC ranking (25%)
  3. Pakistan's recent form (25%)
  4. Venue/conditions factor (15%)
  5. Pakistan Chaos Multiplier (15%) - because PCB drama is a real factor

  Output is EXAGGERATED slightly - this is a hate watch, not ESPN.

LIVE MATCH MODE:
  Real-time loss probability using current match state.
"""

import numpy as np
from typing import Optional


# ============================================
# HEAD-TO-HEAD DATA (since 2022, all formats combined)
# Pakistan's record vs each team
# ============================================

HEAD_TO_HEAD = {
    "india":         {"played": 12, "pak_wins": 1,  "pak_losses": 10, "draws": 1},
    "australia":     {"played": 15, "pak_wins": 4,  "pak_losses": 10, "draws": 1},
    "england":       {"played": 18, "pak_wins": 6,  "pak_losses": 11, "draws": 1},
    "south africa":  {"played": 8,  "pak_wins": 2,  "pak_losses": 6,  "draws": 0},
    "new zealand":   {"played": 14, "pak_wins": 6,  "pak_losses": 7,  "draws": 1},
    "sri lanka":     {"played": 10, "pak_wins": 6,  "pak_losses": 4,  "draws": 0},
    "west indies":   {"played": 8,  "pak_wins": 5,  "pak_losses": 3,  "draws": 0},
    "bangladesh":    {"played": 8,  "pak_wins": 5,  "pak_losses": 3,  "draws": 0},
    "afghanistan":   {"played": 5,  "pak_wins": 3,  "pak_losses": 2,  "draws": 0},
    "zimbabwe":      {"played": 6,  "pak_wins": 5,  "pak_losses": 1,  "draws": 0},
    "ireland":       {"played": 4,  "pak_wins": 2,  "pak_losses": 2,  "draws": 0},
    "usa":           {"played": 1,  "pak_wins": 0,  "pak_losses": 1,  "draws": 0},
    "netherlands":   {"played": 2,  "pak_wins": 1,  "pak_losses": 1,  "draws": 0},
    "nepal":         {"played": 1,  "pak_wins": 1,  "pak_losses": 0,  "draws": 0},
    "hong kong":     {"played": 2,  "pak_wins": 2,  "pak_losses": 0,  "draws": 0},
    "namibia":       {"played": 2,  "pak_wins": 2,  "pak_losses": 0,  "draws": 0},
    "scotland":      {"played": 1,  "pak_wins": 1,  "pak_losses": 0,  "draws": 0},
}

# Approximate ICC T20I/ODI combined rankings (lower = better)
ICC_RANKINGS = {
    "india": 1, "australia": 2, "england": 3, "south africa": 4,
    "new zealand": 5, "west indies": 6, "sri lanka": 7, "pakistan": 8,
    "bangladesh": 9, "afghanistan": 10, "ireland": 11, "zimbabwe": 12,
    "netherlands": 13, "nepal": 14, "usa": 15, "namibia": 16,
    "scotland": 17, "hong kong": 18, "oman": 19, "uae": 20,
}

# Pakistan recent form: last ~10 completed international matches
# True = win, False = loss
PAKISTAN_RECENT_FORM = [
    False,  # vs England, 3rd Test (lost by 8 wkts)
    False,  # vs England, 2nd Test (lost by 194 runs)
    False,  # vs England, 1st Test (lost by innings and 103 runs)
    True,   # vs County XI (warm-up win)
    False,  # vs India, T20 WC 2026 (114 all out, lost by 61 runs)
    True,   # vs Namibia, T20 WC 2026 (won by 102 runs)
    True,   # vs Hong Kong, T20 WC 2026 (abandoned but qualified)
    False,  # vs Sri Lanka, T20 WC 2026 Super 8 (lost)
    False,  # vs New Zealand, ODI (174 all out, lost by 6 wkts)
    False,  # vs New Zealand, T20I (131/9, lost by 7 wkts)
]


def compute_prematch_loss_probability(opponent: str, match_format: str = "ODI", venue: str = "", is_home: bool = False) -> dict:
    """
    Compute pre-match loss probability for an upcoming Pakistan match.

    Uses:
    - H2H record vs this opponent (20%)
    - Opponent ICC ranking (25%)
    - Pakistan recent form (25%)
    - Venue/conditions (15%)
    - Pakistan Chaos Multiplier™ (15%)

    Returns an exaggerated loss probability because this is a hate watch.
    """
    opp_lower = opponent.lower().strip()

    # --- 1. Head-to-Head (20%) ---
    h2h = HEAD_TO_HEAD.get(opp_lower, {"played": 0, "pak_wins": 0, "pak_losses": 0, "draws": 0})
    if h2h["played"] > 0:
        h2h_loss_rate = h2h["pak_losses"] / h2h["played"]
    else:
        h2h_loss_rate = 0.5  # Unknown opponent, coin flip

    h2h_detail = f"{h2h['pak_losses']}L in {h2h['played']} matches since 2022"

    # --- 2. Opponent ICC Ranking (25%) ---
    opp_rank = ICC_RANKINGS.get(opp_lower, 15)
    pak_rank = ICC_RANKINGS.get("pakistan", 8)

    # If opponent is ranked higher (lower number), Pakistan more likely to lose
    # If opponent is ranked below 12, Pakistan should win
    if opp_rank <= 3:
        ranking_loss_factor = 0.75  # Top 3 = Pakistan loses ~75%
    elif opp_rank <= 6:
        ranking_loss_factor = 0.60
    elif opp_rank <= 8:
        ranking_loss_factor = 0.50  # Similar level
    elif opp_rank <= 12:
        ranking_loss_factor = 0.35
    else:
        ranking_loss_factor = 0.20  # Ranked below 12, Pakistan SHOULD win
        # But this is Pakistan - upset potential is always there
        ranking_loss_factor += 0.10  # Even against minnows, 30% chance of embarrassment

    ranking_detail = f"Opponent ranked #{opp_rank}, Pakistan #{pak_rank}"

    # --- 3. Pakistan Recent Form (25%) ---
    wins = sum(1 for r in PAKISTAN_RECENT_FORM if r)
    losses = sum(1 for r in PAKISTAN_RECENT_FORM if not r)
    form_loss_rate = losses / max(len(PAKISTAN_RECENT_FORM), 1)

    form_detail = f"{losses}L, {wins}W in last {len(PAKISTAN_RECENT_FORM)} matches"

    # --- 4. Venue Factor (15%) ---
    if is_home:
        venue_factor = 0.40  # Home advantage, but England 3-0'd them at home so...
    elif "australia" in venue.lower() or "england" in venue.lower() or "south africa" in venue.lower():
        venue_factor = 0.70  # SENA countries = Pakistan's graveyard
    elif "uae" in venue.lower() or "dubai" in venue.lower():
        venue_factor = 0.40  # UAE is practically home
    else:
        venue_factor = 0.55  # Neutral/away

    venue_detail = "Home" if is_home else f"At {venue}" if venue else "Venue TBD"

    # --- 5. Pakistan Chaos Multiplier™ (15%) ---
    # Selection drama, coaching changes, board politics, senior player egos
    chaos_factor = 0.65  # Base chaos level (always high for Pakistan)

    chaos_detail = "PCB politics, coaching carousel, selection drama"

    # --- Weighted calculation ---
    raw_prob = (
        h2h_loss_rate * 0.20 +
        ranking_loss_factor * 0.25 +
        form_loss_rate * 0.25 +
        venue_factor * 0.15 +
        chaos_factor * 0.15
    )

    # --- EXAGGERATION for hate watch ---
    # Bump it up 8-15% because this is Pakistan and they always find new ways to lose
    exaggeration = 0.08 + np.random.uniform(0, 0.07)
    exaggerated_prob = min(0.95, raw_prob + exaggeration)

    loss_pct = round(exaggerated_prob * 100, 1)

    # Generate a roast based on the probability
    if loss_pct >= 80:
        verdict = "💀 Might as well forfeit"
    elif loss_pct >= 70:
        verdict = "🪦 Start writing the post-match excuses"
    elif loss_pct >= 60:
        verdict = "😰 Classic Pakistan choking territory"
    elif loss_pct >= 50:
        verdict = "🎲 Coin flip, but Pakistan finds ways to lose coin flips too"
    elif loss_pct >= 40:
        verdict = "🤞 There's hope... which makes the inevitable loss even more painful"
    else:
        verdict = "😴 They should win this. Key word: SHOULD."

    return {
        "loss_probability": loss_pct,
        "win_probability": round(100 - loss_pct, 1),
        "verdict": verdict,
        "breakdown": {
            "h2h": {"weight": "20%", "value": round(h2h_loss_rate * 100, 1), "detail": h2h_detail, "record": h2h},
            "ranking": {"weight": "25%", "value": round(ranking_loss_factor * 100, 1), "detail": ranking_detail, "opp_rank": opp_rank, "pak_rank": pak_rank},
            "form": {"weight": "25%", "value": round(form_loss_rate * 100, 1), "detail": form_detail, "recent": PAKISTAN_RECENT_FORM},
            "venue": {"weight": "15%", "value": round(venue_factor * 100, 1), "detail": venue_detail},
            "chaos": {"weight": "15%", "value": round(chaos_factor * 100, 1), "detail": chaos_detail},
        },
        "exaggeration_note": "Probabilities are slightly inflated because... well... it's Pakistan",
    }


# ============================================
# LIVE MATCH MODE (kept from before)
# ============================================

COLLAPSE_BASE_RATES = {"ODI": 0.18, "T20I": 0.22, "Test": 0.15}
CHOKE_MULTIPLIER = 1.35
PRESSURE_RR_DECLINE = 0.82


def compute_live_loss_probability(
    match_format: str, innings: int, overs: float, runs: int, wickets: int,
    target: Optional[int] = None, total_overs: Optional[float] = None,
    batting_first: bool = True, opponent: str = "Unknown",
    partnership_balls: int = 0, last_six_overs_runs: Optional[list[int]] = None,
) -> dict:
    """Real-time loss probability from current match state."""
    if total_overs is None:
        total_overs = {"ODI": 50.0, "T20I": 20.0, "Test": 90.0}.get(match_format, 50.0)

    overs_remaining = max(0.1, total_overs - overs)
    wickets_remaining = 10 - wickets

    # Resource calculation
    wicket_resource = _wicket_resources(wickets_remaining)
    over_resource = overs_remaining / total_overs
    resources_remaining = wicket_resource * over_resource

    current_rr = runs / max(overs, 0.1)

    # Chase analysis
    if target is not None and not batting_first:
        runs_needed = target - runs
        required_rr = runs_needed / max(overs_remaining, 0.1)
        chase_difficulty = np.clip(required_rr / max(current_rr, 0.1), 0, 5)
    else:
        runs_needed = 0
        required_rr = 0
        chase_difficulty = 1.0

    # Collapse risk
    collapse_base = COLLAPSE_BASE_RATES.get(match_format, 0.18)
    collapse_risk = collapse_base * (1 + max(0, wickets - 2) * 0.15) if wickets >= 3 else collapse_base * 0.5
    if partnership_balls < 12 and wickets >= 2:
        collapse_risk *= 1.3

    # Loss probability
    if batting_first:
        projected_score = runs + (current_rr * overs_remaining * resources_remaining)
        winning_scores = {"ODI": 280, "T20I": 170, "Test": 350}
        score_ratio = projected_score / winning_scores.get(match_format, 280)
        loss_prob = (1 - np.clip(score_ratio * 0.6, 0, 0.85)) + collapse_risk * 0.3
    else:
        if runs_needed <= 0:
            loss_prob = 0.01
        else:
            base_chase = np.clip(0.3 + (chase_difficulty - 1) * 0.25, 0.1, 0.95)
            loss_prob = base_chase * (0.5 + (1 - resources_remaining) * 0.5) + collapse_risk * 0.35
            if required_rr > 8.0:
                loss_prob *= CHOKE_MULTIPLIER * 0.9

    loss_prob = float(np.clip(loss_prob, 0.02, 0.98))
    collapse_risk = float(np.clip(collapse_risk, 0, 1))

    # Alert level
    if loss_prob > 0.85: alert_level = "MELTDOWN"
    elif loss_prob > 0.70: alert_level = "COLLAPSE_INCOMING"
    elif loss_prob > 0.55: alert_level = "CHOKING"
    elif loss_prob > 0.40: alert_level = "NERVOUS"
    else: alert_level = "STABLE"

    # Key factors
    key_factors = []
    if wickets >= 5: key_factors.append(f"🚨 {wickets} wickets down - deep trouble")
    if wickets >= 3 and overs < total_overs * 0.3: key_factors.append("⚠️ Early wickets - collapse pattern forming")
    if not batting_first and required_rr > 10: key_factors.append(f"📈 Required rate {required_rr:.1f} - nearly impossible")
    elif not batting_first and required_rr > 7: key_factors.append(f"📈 Required rate climbing to {required_rr:.1f}")
    if collapse_risk > 0.4: key_factors.append("💀 High collapse probability based on Pakistan patterns")
    if partnership_balls < 12 and wickets >= 2: key_factors.append("🔄 Short partnerships - no stability")
    if not key_factors: key_factors.append("📊 Match situation is developing")

    historical = _find_historical_comparison(match_format, runs, wickets, overs, target, batting_first)
    proj_score = int(runs + current_rr * overs_remaining) if batting_first else (target or int(runs + current_rr * overs_remaining))

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


def _wicket_resources(w: int) -> float:
    return {10:1.0,9:0.91,8:0.81,7:0.70,6:0.58,5:0.46,4:0.34,3:0.23,2:0.13,1:0.05,0:0.0}.get(w, 0.0)


def _find_historical_comparison(fmt, runs, wkts, overs, target, bat_first):
    if wkts >= 5 and overs < 25 and fmt == "ODI":
        return "Reminiscent of 2023 WC vs India - collapsed to 191 all out"
    if wkts >= 4 and overs < 10 and fmt == "T20I":
        return "Similar to T20 WC 2024 group stage - top order fell apart"
    if not bat_first and target:
        rr = (target - runs) / max(50 - overs if fmt == "ODI" else 20 - overs, 0.1)
        if rr > 9 and fmt == "ODI": return "Pakistan have never chased at 9+ RPO for more than 10 overs"
        if rr > 12 and fmt == "T20I": return "Similar to 2021 semi-final vs Australia - didn't end well"
    if wkts <= 1 and overs > 15 and fmt == "ODI":
        return "Good position but Pakistan went from 150/1 to 191 all out vs India in 2023"
    return "Pakistan are capable of miracles and disasters equally"
