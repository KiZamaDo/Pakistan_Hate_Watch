"""
Pakistan T20I Fraud Detection Engine v3
=======================================
T20I-only. Hard rules:
- ICC knockout avg < 15 = CERTIFIED FRAUD (Babar 13.7, Rizwan 13.6)
- T20 WC powerplay SR < 100 = CERTIFIED FRAUD (Babar 86, Rizwan 98)
- SR gap associates vs test nations > 25 = stat-padding fraud
- Fakhar's 132+ SR and 6 MOMs vs test nations = NOT a fraud

Components:
1. Match-Winning Ability (30%): MOMs vs Test nations, chase wins, knockout performance
2. Strike Rate Analysis (25%): T20I SR, SR vs Test nations, stat-padding gap
3. ICC Tournament Performance (25%): WC avg/SR, powerplay SR, knockout avg
4. Consistency & Trend (20%): form direction, big match failure rate
"""

import numpy as np

FRAUD_THRESHOLDS = {
    "certified-fraud": (0, 25),
    "suspect": (25, 40),
    "underperformer": (40, 55),
    "inconsistent": (55, 70),
    "redeemable": (70, 100),
}


def compute_fraud_score(player: dict) -> dict:
    stats = player.get("stats", {})
    trends = player.get("performance_trend", [])
    role = player.get("role", "Batsman")

    mw = _match_winning(stats, role)
    sr = _strike_rate(stats, role)
    icc = _icc_tournament(stats, role)
    con = _consistency(stats, trends, role)

    overall = mw * 0.30 + sr * 0.25 + icc * 0.25 + con * 0.20
    overall = float(np.clip(overall, 0, 100))

    fraud_rating = "redeemable"
    for rating, (low, high) in FRAUD_THRESHOLDS.items():
        if low <= overall < high:
            fraud_rating = rating
            break

    analysis = _make_analysis(player["name"], role, mw, sr, icc, con, overall, stats)

    return {
        "player_id": player.get("id", ""),
        "player_name": player["name"],
        "fraud_rating": fraud_rating,
        "overall_score": round(overall, 1),
        "components": {
            "match_winning": {"score": round(mw, 1), "weight": "30%", "description": "MOM awards vs Test nations, successful chases, ICC knockouts"},
            "strike_rate": {"score": round(sr, 1), "weight": "25%", "description": "T20I strike rate, SR vs real teams, stat-padding gap"},
            "icc_tournament": {"score": round(icc, 1), "weight": "25%", "description": "T20 WC performance, knockout avg, powerplay SR"},
            "consistency": {"score": round(con, 1), "weight": "20%", "description": "Form trajectory and reliability"},
        },
        "analysis": analysis,
    }


def _match_winning(stats: dict, role: str) -> float:
    mom_test = stats.get("mom_vs_test_nations", 0)
    mom_assoc = stats.get("mom_vs_associates", 0)
    matches = max(stats.get("matches", 1), 1)

    # MOM quality ratio
    total_mom = mom_test + mom_assoc
    mom_quality = (mom_test / total_mom) if total_mom > 0 else 0

    # MOM rate vs test nations (per match)
    mom_rate = mom_test / matches

    score = mom_quality * 35 + mom_rate * 500

    # Chase success vs top teams
    if role != "Bowler":
        success = stats.get("successful_chases_top_teams", 0)
        failed = stats.get("failed_chases_top_teams", 0)
        total_chases = success + failed
        if total_chases >= 3:
            chase_rate = success / total_chases
            if chase_rate >= 0.5:
                score += 25
            elif chase_rate >= 0.35:
                score += 15
            elif chase_rate >= 0.2:
                score += 5
            else:
                score -= 5  # Less than 20% chase success = liability

    # ICC knockout performance
    ko_avg = stats.get("icc_knockout_avg", 0)
    ko_inn = stats.get("icc_knockout_innings", 0)
    if role != "Bowler" and ko_inn >= 3:
        if ko_avg >= 40:
            score += 25
        elif ko_avg >= 25:
            score += 15
        elif ko_avg >= 15:
            score += 5
        else:
            score -= 15  # Sub-15 knockout avg = FRAUD signal

    # Bowler: avg vs test nations
    if role == "Bowler":
        avg_test = stats.get("avg_vs_test_nations", 30)
        if avg_test < 23:
            score += 20
        elif avg_test < 27:
            score += 10
        else:
            score -= 5

    return float(np.clip(score, 0, 100))


def _strike_rate(stats: dict, role: str) -> float:
    if role == "Bowler":
        eco = stats.get("economy_rate", 8.0)
        death_eco = stats.get("death_overs_economy", 10.0)
        score = 70 if eco <= 6.5 else 55 if eco <= 7.2 else 35 if eco <= 8.0 else 15
        if death_eco > 10:
            score -= 15
        elif death_eco > 9:
            score -= 8
        return float(np.clip(score, 0, 100))

    sr = stats.get("strike_rate", 120)
    sr_test = stats.get("sr_vs_test_nations", sr)
    sr_assoc = stats.get("sr_vs_associates", sr)

    # Overall SR scoring — harsh below 130
    if sr >= 155:
        score = 95
    elif sr >= 145:
        score = 80
    elif sr >= 140:
        score = 70
    elif sr >= 135:
        score = 60
    elif sr >= 130:
        score = 45
    elif sr >= 125:
        score = 25  # 125 is a problem in T20s
    elif sr >= 120:
        score = 10  # 120 is criminal
    else:
        score = 0   # Sub-120 = actively destroying the team

    # Stat-padding gap penalty
    sr_gap = sr_assoc - sr_test
    if sr_gap > 25:
        score -= 25  # Massive stat-padding — Babar/Rizwan territory
    elif sr_gap > 15:
        score -= 12
    elif sr_gap < 10:
        score += 10  # Honest player — same SR against everyone

    return float(np.clip(score, 0, 100))


def _icc_tournament(stats: dict, role: str) -> float:
    if role == "Bowler":
        avg_test = stats.get("avg_vs_test_nations", 30)
        eco = stats.get("economy_rate", 8.0)
        score = max(0, 65 - (avg_test - 20) * 3)
        if eco > 8:
            score -= 10
        return float(np.clip(score, 0, 100))

    wc_sr = stats.get("t20_wc_sr", 0)
    wc_avg = stats.get("t20_wc_avg", 0)
    wc_pp_sr = stats.get("t20_wc_powerplay_sr", 0)
    ko_avg = stats.get("icc_knockout_avg", 0)
    ko_inn = stats.get("icc_knockout_innings", 0)
    matches = stats.get("matches", 0)

    score = 0

    # WC Strike Rate — MOST IMPORTANT
    if wc_sr >= 155:
        score += 40
    elif wc_sr >= 140:
        score += 32
    elif wc_sr >= 130:
        score += 22
    elif wc_sr >= 120:
        score += 12
    elif wc_sr > 0:
        score += 2   # Sub-120 WC SR = bilateral merchant confirmed

    # WC average
    if wc_avg >= 60:
        score += 20
    elif wc_avg >= 40:
        score += 15
    elif wc_avg >= 25:
        score += 8
    elif wc_avg > 0:
        score += 2

    # T20 WC POWERPLAY SR — the killer metric
    if wc_pp_sr > 0:
        if wc_pp_sr >= 145:
            score += 20
        elif wc_pp_sr >= 130:
            score += 12
        elif wc_pp_sr >= 110:
            score += 5
        elif wc_pp_sr >= 100:
            score -= 5   # Below 100 PP SR in a WC is bad
        else:
            score -= 20  # Sub-100 = Babar's 86 territory. FRAUD.

    # ICC knockout avg
    if ko_inn >= 3:
        if ko_avg >= 40:
            score += 15
        elif ko_avg >= 25:
            score += 8
        elif ko_avg >= 15:
            score += 2
        elif ko_avg < 10:
            score -= 20  # Sub-10 knockout avg = Wide Ball Nawaz

    # Never played a WC = neutral
    if wc_sr == 0 and wc_avg == 0 and matches > 0:
        score = 30

    return float(np.clip(score, 0, 100))


def _consistency(stats: dict, trends: list, role: str) -> float:
    if not trends or len(trends) < 2:
        return 40.0

    # Use SR trend for batsmen, bowling avg for bowlers
    if role != "Bowler":
        values = [t.get("strike_rate", 120) for t in trends if t.get("matches", 0) > 0]
    else:
        values = [50 - t.get("average", 30) for t in trends if t.get("matches", 0) > 0]

    if len(values) < 2:
        return 40.0

    x = np.arange(len(values))
    slope = np.polyfit(x, values, 1)[0]
    score = 50 + slope * 3

    # Big match failure rate
    failures = stats.get("big_match_failures", 0)
    matches = max(stats.get("matches", 1), 1)
    rate = failures / matches
    if rate > 0.12:
        score -= 20
    elif rate > 0.08:
        score -= 10

    # Dropped from squad (last period has 0 matches)
    if trends[-1].get("matches", 0) == 0:
        score -= 15

    return float(np.clip(score, 0, 100))


def _make_analysis(name: str, role: str, mw: float, sr: float, icc: float, con: float, overall: float, stats: dict) -> str:
    parts = []
    sr_val = stats.get("strike_rate", 0)
    sr_test = stats.get("sr_vs_test_nations", 0)
    wc_sr = stats.get("t20_wc_sr", 0)
    wc_pp_sr = stats.get("t20_wc_powerplay_sr", 0)
    ko_avg = stats.get("icc_knockout_avg", 0)
    ko_inn = stats.get("icc_knockout_innings", 0)
    mom_test = stats.get("mom_vs_test_nations", 0)

    if role != "Bowler":
        if wc_pp_sr > 0 and wc_pp_sr < 100:
            parts.append(f"T20 WC powerplay SR of {wc_pp_sr} — among the worst in World Cup history")
        if ko_inn >= 3 and ko_avg < 15:
            parts.append(f"ICC knockout average of {ko_avg} — certified big-game ghost")
        if sr_val < 130 and role != "Bowler":
            parts.append(f"T20I SR of {sr_val} is below modern standards — consuming balls others could use")
        gap = stats.get("sr_vs_associates", 0) - sr_test
        if gap > 20:
            parts.append(f"SR drops {gap:.0f} points against Test nations — classic stat-padder")
        if mom_test <= 2 and stats.get("matches", 0) > 50:
            parts.append(f"Only {mom_test} MOMs vs Test nations in {stats.get('matches', 0)} matches")
    else:
        eco = stats.get("economy_rate", 0)
        death = stats.get("death_overs_economy", 0)
        if death > 10:
            parts.append(f"Death overs economy of {death} — gets carted when it matters")
        if eco > 8:
            parts.append(f"Overall economy of {eco} — too expensive for T20Is")

    if not parts:
        parts.append(f"{name} delivers enough to justify selection")

    return ". ".join(parts) + "."


def get_fraud_rating_label(rating: str) -> dict:
    labels = {
        "certified-fraud": {"label": "CERTIFIED FRAUD", "emoji": "🚨", "color": "#ef4444", "description": "Bilateral merchant. Fails when it matters."},
        "suspect": {"label": "SUSPECT", "emoji": "🔍", "color": "#f59e0b", "description": "Pattern of underperformance in big games."},
        "underperformer": {"label": "UNDERPERFORMER", "emoji": "📉", "color": "#eab308", "description": "Has talent but rarely delivers to potential."},
        "inconsistent": {"label": "INCONSISTENT", "emoji": "🎲", "color": "#3b82f6", "description": "Flashes of brilliance in mediocrity."},
        "redeemable": {"label": "REDEEMABLE", "emoji": "🤞", "color": "#00a651", "description": "Shows enough to keep hope alive."},
    }
    return labels.get(rating, labels["inconsistent"])
