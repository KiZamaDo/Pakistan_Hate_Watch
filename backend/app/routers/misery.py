"""
Misery Dashboard Router - Since 2022 only
==========================================
Proper categories, real tournament record, home series, h2h.
"""

from fastapi import APIRouter
from collections import Counter
from app.data.defeats import RECENT_DEFEATS, TOURNAMENT_RECORD, HOME_SERIES, HEAD_TO_HEAD

router = APIRouter()


@router.get("/stats")
def get_misery_stats():
    defeats = RECENT_DEFEATS

    # Category breakdown (humiliating / embarrassing / expected)
    cat_counts = Counter(d["category"] for d in defeats)

    # By format
    fmt_counts = Counter(d["format"] for d in defeats)

    # By opponent
    opp_counts = Counter(d["opponent"] for d in defeats)
    by_opponent = [{"opponent": o, "defeats": c} for o, c in opp_counts.most_common()]

    # Avg misery
    avg_misery = sum(d["misery"] for d in defeats) / max(len(defeats), 1)

    # Worst defeat
    worst = max(defeats, key=lambda d: d["misery"])

    # Tournament record
    tournaments_lost = sum(1 for t in TOURNAMENT_RECORD if not t["won"])

    # Home series record
    home_won = sum(1 for s in HOME_SERIES if s["won"])
    home_lost = sum(1 for s in HOME_SERIES if not s["won"])

    # Overall W/L since 2022 from h2h
    total_won = sum(v["won"] for v in HEAD_TO_HEAD.values())
    total_lost = sum(v["lost"] for v in HEAD_TO_HEAD.values())

    # Humiliating = big margin losses
    humiliating = [d for d in defeats if d["category"] == "humiliating"]
    # Embarrassing = lost to minnows
    embarrassing = [d for d in defeats if d["category"] == "embarrassing"]

    return {
        "period": "Since January 2022",
        "total_defeats": len(defeats),
        "overall_record": {"won": total_won, "lost": total_lost, "win_pct": round(total_won / max(total_won + total_lost, 1) * 100, 1)},
        "average_misery": round(avg_misery, 1),

        "category_breakdown": {
            "humiliating": {"count": cat_counts.get("humiliating", 0), "label": "Humiliating", "description": "Lost by massive margins (innings defeat, 100+ runs, 8+ wickets)", "matches": [{"opponent": d["opponent"], "margin": d["margin"], "date": d["date"], "tournament": d.get("tournament")} for d in humiliating]},
            "embarrassing": {"count": cat_counts.get("embarrassing", 0), "label": "Embarrassing", "description": "Lost to minnow or lower-ranked teams", "matches": [{"opponent": d["opponent"], "margin": d["margin"], "date": d["date"], "tournament": d.get("tournament")} for d in embarrassing]},
            "expected": {"count": cat_counts.get("expected", 0), "label": "Expected", "description": "Lost to higher-ranked teams in competitive matches"},
        },

        "format_breakdown": dict(fmt_counts),

        "defeats_by_opponent": by_opponent,

        "tournament_record": {
            "total": len(TOURNAMENT_RECORD),
            "trophies_won": 0,
            "tournaments": TOURNAMENT_RECORD,
            "summary": f"0 trophies from {len(TOURNAMENT_RECORD)} ICC events since 2022",
        },

        "home_series": {
            "won": home_won,
            "lost": home_lost,
            "series": HOME_SERIES,
            "summary": f"Won {home_won}, Lost {home_lost} home series since 2022",
        },

        "head_to_head": {
            opponent: {**record, "win_pct": round(record["won"] / max(record["played"], 1) * 100, 1)}
            for opponent, record in sorted(HEAD_TO_HEAD.items(), key=lambda x: x[1]["lost"], reverse=True)
        },

        "worst_defeat": worst,

        "lowlights": [
            {"event": "Lost to USA in Super Over - T20 WC 2024", "misery": 10, "category": "embarrassing"},
            {"event": "Lost to Zimbabwe by 1 run - T20 WC 2022", "misery": 10, "category": "embarrassing"},
            {"event": "114 all out vs India - T20 WC 2026", "misery": 9, "category": "humiliating"},
            {"event": "Lost by an innings at Old Trafford - 2026", "misery": 9, "category": "humiliating"},
            {"event": "Lost to Afghanistan at ODI WC 2023", "misery": 9, "category": "embarrassing"},
            {"event": "Group stage exit - T20 WC 2024", "misery": 10, "category": "embarrassing"},
        ],

        "fun_facts": [
            "Pakistan have been eliminated from a World Cup by USA 🇺🇸",
            "0 ICC trophies since 2022 across 5 tournaments",
            f"Win rate of {round(total_won / max(total_won + total_lost, 1) * 100)}% since 2022",
            "Lost a home Test series 0-3 to England in 2022 - first time ever",
            "Hosted Champions Trophy 2025 and still couldn't win it",
            f"{cat_counts.get('humiliating', 0)} defeats by massive margins since 2022",
            "Lost to Zimbabwe by 1 run at T20 WC 2022. ONE. RUN.",
            f"Lost to {len(set(d['opponent'] for d in embarrassing))} different minnow/lower-ranked teams",
        ],
    }
