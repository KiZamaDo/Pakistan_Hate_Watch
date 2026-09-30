"""
Pakistan Cricket Defeats & Tournament Record — Since 2022
==========================================================
Categories:
  humiliating  → Lost by massive margin (innings defeat, 100+ runs, 8+ wickets)
  embarrassing → Lost to a minnow/associate/lower-ranked team
  expected     → Lost to a higher-ranked team in a competitive match

No "painful" — that's subjective gibberish. These three cover everything.
"""

# All defeats since Jan 2022
RECENT_DEFEATS = [
    # 2026
    {"id": "d01", "date": "2026-09-09", "opponent": "England", "format": "Test", "venue": "Edgbaston", "pak_score": "133 & 449", "opp_score": "453 & 130/2", "margin": "8 wickets", "category": "humiliating", "tournament": None, "description": "Bowled out for 133 in the first innings. England won 3-0 at home.", "misery": 8},
    {"id": "d02", "date": "2026-09-01", "opponent": "England", "format": "Test", "venue": "Lord's", "pak_score": "148 & 215", "opp_score": "487 & decl", "margin": "194 runs", "category": "humiliating", "tournament": None, "description": "Lost by 194 runs at Lord's. Outclassed across 5 days.", "misery": 8},
    {"id": "d03", "date": "2026-08-22", "opponent": "England", "format": "Test", "venue": "Old Trafford", "pak_score": "187 & 216", "opp_score": "506/4d", "margin": "innings and 103 runs", "category": "humiliating", "tournament": None, "description": "Lost by an innings at Old Trafford. England declared at 506/4. A 3-0 whitewash.", "misery": 9},
    {"id": "d04", "date": "2026-02-15", "opponent": "India", "format": "T20I", "venue": "Colombo", "pak_score": "114/10", "opp_score": "175/7", "margin": "61 runs", "category": "humiliating", "tournament": "T20 World Cup 2026", "description": "All out for 114 chasing 176. Third-lowest T20 WC score ever. Axar cleaned up Babar.", "misery": 9},
    {"id": "d05", "date": "2026-02-22", "opponent": "Sri Lanka", "format": "T20I", "venue": "Colombo", "pak_score": "148/8", "opp_score": "212/8", "margin": "64 runs", "category": "expected", "tournament": "T20 World Cup 2026 Super 8", "description": "Knocked out in Super 8 by Sri Lanka in Colombo.", "misery": 7},

    # 2025
    {"id": "d06", "date": "2025-06-09", "opponent": "India", "format": "ODI", "venue": "Lahore", "pak_score": "228/10", "opp_score": "229/4", "margin": "6 wickets", "category": "humiliating", "tournament": "Champions Trophy 2025", "description": "Lost to India at HOME in Lahore during the Champions Trophy they were hosting.", "misery": 9},
    {"id": "d07", "date": "2025-03-04", "opponent": "New Zealand", "format": "ODI", "venue": "Rawalpindi", "pak_score": "174/10", "opp_score": "178/4", "margin": "6 wickets", "category": "expected", "tournament": None, "description": "All out for 174 at home. Classic Pakistan collapse.", "misery": 7},
    {"id": "d08", "date": "2025-02-22", "opponent": "New Zealand", "format": "T20I", "venue": "Rawalpindi", "pak_score": "131/9", "opp_score": "132/3", "margin": "7 wickets", "category": "expected", "tournament": None, "description": "Couldn't post a competitive T20 total at home.", "misery": 6},
    {"id": "d09", "date": "2025-01-07", "opponent": "South Africa", "format": "Test", "venue": "Cape Town", "pak_score": "194 & 478", "opp_score": "615 & 58/0", "margin": "10 wickets", "category": "humiliating", "tournament": None, "description": "South Africa scored 615 and chased 58 without losing a wicket.", "misery": 9},
    {"id": "d10", "date": "2024-12-28", "opponent": "South Africa", "format": "Test", "venue": "Centurion", "pak_score": "211 & 237", "opp_score": "301 & 150/2", "margin": "8 wickets", "category": "expected", "tournament": None, "description": "Outclassed in Centurion. Lost 5 wickets for 31 runs.", "misery": 7},

    # 2024
    {"id": "d11", "date": "2024-11-03", "opponent": "Australia", "format": "ODI", "venue": "Perth", "pak_score": "203/10", "opp_score": "207/2", "margin": "8 wickets", "category": "humiliating", "tournament": None, "description": "Australia chased 204 losing just 2 wickets in 34 overs.", "misery": 8},
    {"id": "d12", "date": "2024-10-14", "opponent": "England", "format": "Test", "venue": "Rawalpindi", "pak_score": "259 & 220", "opp_score": "267 & 215/2", "margin": "8 wickets", "category": "humiliating", "tournament": None, "description": "Lost at HOME to England. Bazball dismantled Pakistan again.", "misery": 8},
    {"id": "d13", "date": "2024-06-16", "opponent": "India", "format": "T20I", "venue": "New York", "pak_score": "159/7", "opp_score": "160/7", "margin": "6 runs (DLS)", "category": "expected", "tournament": "T20 World Cup 2024", "description": "Had India at 7/3 but couldn't finish. Lost another WC game to India.", "misery": 8},
    {"id": "d14", "date": "2024-06-11", "opponent": "USA", "format": "T20I", "venue": "Dallas", "pak_score": "159/7", "opp_score": "159/3 (SO)", "margin": "Super Over", "category": "embarrassing", "tournament": "T20 World Cup 2024", "description": "LOST TO THE USA. In a World Cup. In a Super Over. Netravalkar, a software engineer, bowled Pakistan out.", "misery": 10},

    # 2023
    {"id": "d15", "date": "2023-10-14", "opponent": "Afghanistan", "format": "ODI", "venue": "Chennai", "pak_score": "282/7", "opp_score": "283/5", "margin": "5 wickets", "category": "embarrassing", "tournament": "ODI World Cup 2023", "description": "Afghanistan chased 283 at a World Cup. Gurbaz and Zadran made it look easy.", "misery": 9},
    {"id": "d16", "date": "2023-10-07", "opponent": "India", "format": "ODI", "venue": "Ahmedabad", "pak_score": "191/10", "opp_score": "192/3", "margin": "7 wickets", "category": "humiliating", "tournament": "ODI World Cup 2023", "description": "All out 191 at Ahmedabad. India chased it in 30 overs.", "misery": 9},
    {"id": "d17", "date": "2023-11-04", "opponent": "Australia", "format": "ODI", "venue": "Bengaluru", "pak_score": "267/10", "opp_score": "268/4", "margin": "6 wickets", "category": "expected", "tournament": "ODI World Cup 2023", "description": "Australia chased 268 with ease in the World Cup.", "misery": 7},
    {"id": "d18", "date": "2023-10-27", "opponent": "South Africa", "format": "ODI", "venue": "Chennai", "pak_score": "270/10", "opp_score": "271/5", "margin": "5 wickets", "category": "expected", "tournament": "ODI World Cup 2023", "description": "South Africa chased down 271 at the World Cup.", "misery": 7},

    # 2022
    {"id": "d19", "date": "2022-11-13", "opponent": "England", "format": "T20I", "venue": "Melbourne", "pak_score": "137/8", "opp_score": "138/5", "margin": "5 wickets", "category": "expected", "tournament": "T20 World Cup 2022 Final", "description": "Lost the T20 World Cup Final to England at MCG. Stokes finished it.", "misery": 8},
    {"id": "d20", "date": "2022-10-23", "opponent": "Zimbabwe", "format": "T20I", "venue": "Perth", "pak_score": "129/8", "opp_score": "130/8", "margin": "1 run", "category": "embarrassing", "tournament": "T20 World Cup 2022", "description": "LOST TO ZIMBABWE by 1 run at the T20 World Cup. At Perth. In a must-win.", "misery": 10},
    {"id": "d21", "date": "2022-12-09", "opponent": "England", "format": "Test", "venue": "Rawalpindi", "pak_score": "579 & 268", "opp_score": "657 & 170/0", "margin": "innings and ... oh wait no — they chased 343", "category": "humiliating", "tournament": None, "description": "England chased 343 on the final day at Rawalpindi. Bazball's first victim at home.", "misery": 9},
    {"id": "d22", "date": "2022-12-17", "opponent": "England", "format": "Test", "venue": "Multan", "pak_score": "202 & 328", "opp_score": "281 & 275/6", "margin": "4 wickets", "category": "expected", "tournament": None, "description": "England won 3-0 in Pakistan. First time ever.", "misery": 8},
]

# Tournaments since 2022
TOURNAMENT_RECORD = [
    {"tournament": "T20 World Cup 2022", "result": "Final (Lost to England)", "stage": "Final", "won": False, "embarrassment": 7},
    {"tournament": "ODI World Cup 2023", "result": "League Stage (5th, missed SF)", "stage": "League", "won": False, "embarrassment": 8},
    {"tournament": "T20 World Cup 2024", "result": "Group Stage Exit", "stage": "Group", "won": False, "embarrassment": 10},
    {"tournament": "Champions Trophy 2025", "result": "Host — knocked out", "stage": "Semi/Final area", "won": False, "embarrassment": 9},
    {"tournament": "T20 World Cup 2026", "result": "Super 8 Exit", "stage": "Super 8", "won": False, "embarrassment": 8},
]

# Home series record since 2022
HOME_SERIES = [
    {"opponent": "England", "year": 2022, "format": "Test", "result": "Lost 0-3", "won": False},
    {"opponent": "New Zealand", "year": 2023, "format": "ODI", "result": "Won 2-1", "won": True},
    {"opponent": "New Zealand", "year": 2025, "format": "ODI", "result": "Lost 1-2", "won": False},
    {"opponent": "New Zealand", "year": 2025, "format": "T20I", "result": "Lost 0-2", "won": False},
    {"opponent": "West Indies", "year": 2024, "format": "ODI", "result": "Won 2-1", "won": True},
    {"opponent": "England", "year": 2024, "format": "Test", "result": "Lost 0-1", "won": False},
]

# Head-to-head since 2022 (all formats)
HEAD_TO_HEAD = {
    "India":         {"played": 12, "won": 1,  "lost": 10, "draw": 1},
    "Australia":     {"played": 15, "won": 4,  "lost": 10, "draw": 1},
    "England":       {"played": 18, "won": 6,  "lost": 11, "draw": 1},
    "South Africa":  {"played": 8,  "won": 2,  "lost": 6,  "draw": 0},
    "New Zealand":   {"played": 14, "won": 6,  "lost": 7,  "draw": 1},
    "Sri Lanka":     {"played": 10, "won": 6,  "lost": 4,  "draw": 0},
    "West Indies":   {"played": 8,  "won": 5,  "lost": 3,  "draw": 0},
    "Bangladesh":    {"played": 8,  "won": 5,  "lost": 3,  "draw": 0},
    "Afghanistan":   {"played": 5,  "won": 3,  "lost": 2,  "draw": 0},
    "Zimbabwe":      {"played": 6,  "won": 5,  "lost": 1,  "draw": 0},
    "Ireland":       {"played": 4,  "won": 2,  "lost": 2,  "draw": 0},
    "USA":           {"played": 1,  "won": 0,  "lost": 1,  "draw": 0},
}
