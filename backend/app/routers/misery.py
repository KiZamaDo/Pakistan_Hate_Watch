"""
Misery Dashboard Router — Aggregated stats of Pakistan cricket pain
"""

from fastapi import APIRouter
from collections import Counter

from app.data.defeats import RECENT_DEFEATS, TOURNAMENT_EXITS

router = APIRouter()


@router.get("/stats")
def get_misery_stats():
    """
    Aggregated misery statistics — the numbers that tell the whole story.
    """
    # Defeats by severity
    severity_counts = Counter(d["severity"] for d in RECENT_DEFEATS)

    # Defeats by format
    format_counts = Counter(d["format"] for d in RECENT_DEFEATS)

    # Defeats by opponent
    opponent_counts = Counter(d["opponent"] for d in RECENT_DEFEATS)
    defeats_by_opponent = [
        {"opponent": opp, "defeats": count}
        for opp, count in opponent_counts.most_common()
    ]

    # Average misery rating
    avg_misery = sum(d["misery_rating"] for d in RECENT_DEFEATS) / max(len(RECENT_DEFEATS), 1)

    # Worst defeat
    worst = max(RECENT_DEFEATS, key=lambda d: d["misery_rating"])

    # Monthly misery (group by year-month)
    monthly = {}
    for d in RECENT_DEFEATS:
        month_key = d["date"][:7]  # YYYY-MM
        if month_key not in monthly:
            monthly[month_key] = {"month": month_key, "defeats": 0, "total_misery": 0}
        monthly[month_key]["defeats"] += 1
        monthly[month_key]["total_misery"] += d["misery_rating"]

    monthly_misery = []
    for m in sorted(monthly.values(), key=lambda x: x["month"]):
        m["avg_misery"] = round(m["total_misery"] / max(m["defeats"], 1), 1)
        monthly_misery.append(m)

    # Humiliation index: weighted score of all defeats
    humiliation_index = sum(
        d["misery_rating"] * (2 if d["severity"] == "humiliating" else 1)
        for d in RECENT_DEFEATS
    )

    return {
        "total_defeats_tracked": len(RECENT_DEFEATS),
        "total_tournament_exits": len(TOURNAMENT_EXITS),
        "humiliation_index": humiliation_index,
        "average_misery_rating": round(avg_misery, 1),
        "severity_breakdown": {
            "humiliating": severity_counts.get("humiliating", 0),
            "painful": severity_counts.get("painful", 0),
            "embarrassing": severity_counts.get("embarrassing", 0),
            "expected": severity_counts.get("expected", 0),
        },
        "format_breakdown": {
            "Test": format_counts.get("Test", 0),
            "ODI": format_counts.get("ODI", 0),
            "T20I": format_counts.get("T20I", 0),
        },
        "defeats_by_opponent": defeats_by_opponent,
        "monthly_misery": monthly_misery,
        "worst_defeat": worst,
        "lowest_points": [
            {"event": "Lost to USA in Super Over at T20 WC 2024", "misery": 10},
            {"event": "Group stage exit T20 WC 2024", "misery": 10},
            {"event": "Lost to Afghanistan at ODI WC 2023", "misery": 9},
            {"event": "191 all out vs India at WC 2023", "misery": 9},
            {"event": "Wade's 3 sixes — T20 WC 2021 Semi-Final", "misery": 9},
        ],
        "fun_facts": [
            "Pakistan have been eliminated from the group stage of a World Cup by USA 🇺🇸",
            "They've lost more ICC knockouts than they've won since 2017",
            "Pakistan's tail (8-11) averages 7.8 in ODIs since 2022",
            "The team has had 7 different coaching setups in 5 years",
            "Pakistan lost to Ireland at the 2007 World Cup — a result linked to a coaching tragedy",
        ],
    }
