"""
Upcoming Pakistan Matches with Loss Probability Factors
======================================================
Each match is rated on multiple factors that feed into the
Loss Probability Engine. Factors with negative impact = bad for Pakistan.

Matches with >60% computed loss probability = HATE WATCH 🔥
"""

UPCOMING_MATCHES = [
    {
        "id": "um1",
        "date": "2026-10-15",
        "opponent": "India",
        "opponent_flag": "🇮🇳",
        "format": "ODI",
        "venue": "Dubai International Stadium",
        "series": "Asia Cup 2026",
        "factors": [
            {
                "factor": "Pakistan vs India ICC Event Record",
                "impact": -35,
                "description": "Pakistan have lost most ICC event encounters against India in recent years",
            },
            {
                "factor": "Batting Collapse Risk",
                "impact": -25,
                "description": "Pakistan top order averages under 25 in knockout-pressure games since 2023",
            },
            {
                "factor": "Neutral Venue (Dubai)",
                "impact": 5,
                "description": "Dubai is practically a home ground - slight advantage",
            },
            {
                "factor": "Pakistan Chaos Factor™",
                "impact": -15,
                "description": "Selection drama, coaching changes, and internal politics are peaking",
            },
        ],
    },
    {
        "id": "um2",
        "date": "2026-10-20",
        "opponent": "Sri Lanka",
        "opponent_flag": "🇱🇰",
        "format": "ODI",
        "venue": "Dubai International Stadium",
        "series": "Asia Cup 2026",
        "factors": [
            {
                "factor": "Head-to-Head Record",
                "impact": 15,
                "description": "Pakistan have a decent record vs Sri Lanka in recent ODIs",
            },
            {
                "factor": "Sri Lanka Rising Form",
                "impact": -20,
                "description": "Sri Lanka have been competitive and unpredictable lately",
            },
            {
                "factor": "Pakistan Overconfidence Factor",
                "impact": -15,
                "description": "Pakistan underperform against teams they consider 'easy beats'",
            },
            {
                "factor": "Dubai Conditions",
                "impact": 10,
                "description": "Familiar conditions favor Pakistan slightly",
            },
        ],
    },
    {
        "id": "um3",
        "date": "2026-11-10",
        "opponent": "Australia",
        "opponent_flag": "🇦🇺",
        "format": "Test",
        "venue": "Gabba, Brisbane",
        "series": "Australia Tour 2026-27",
        "factors": [
            {
                "factor": "Fortress Gabba",
                "impact": -40,
                "description": "Australia are nearly unbeatable at the Gabba. Pakistan's pace wilts in Aussie conditions.",
            },
            {
                "factor": "Aussie Pace Battery",
                "impact": -30,
                "description": "Australia's home pace attack is lethal vs Pakistan's fragile batting",
            },
            {
                "factor": "Pakistan Away Test Record",
                "impact": -25,
                "description": "Pakistan have won just 2 Tests in Australia since 1995",
            },
            {
                "factor": "First Test Slow Start",
                "impact": -10,
                "description": "Pakistan historically start slow on overseas tours",
            },
        ],
    },
    {
        "id": "um4",
        "date": "2026-11-22",
        "opponent": "Australia",
        "opponent_flag": "🇦🇺",
        "format": "Test",
        "venue": "MCG, Melbourne",
        "series": "Australia Tour 2026-27",
        "factors": [
            {
                "factor": "MCG Bounce & Pace",
                "impact": -30,
                "description": "MCG pitch suits Australia's pace attack",
            },
            {
                "factor": "Likely 0-1 Down Already",
                "impact": -20,
                "description": "If they lost the Gabba Test, morale will be in the gutter",
            },
            {
                "factor": "Boxing Day Pressure",
                "impact": -15,
                "description": "100K crowd, biggest stage - Pakistan crumble under this spotlight",
            },
            {
                "factor": "Slight MCG Familiarity",
                "impact": 5,
                "description": "More games at MCG than Gabba - marginal comfort",
            },
        ],
    },
    {
        "id": "um5",
        "date": "2026-12-05",
        "opponent": "Australia",
        "opponent_flag": "🇦🇺",
        "format": "T20I",
        "venue": "SCG, Sydney",
        "series": "Australia Tour 2026-27",
        "factors": [
            {
                "factor": "T20 is Pakistan's Stronger Format",
                "impact": 15,
                "description": "Pakistan are more competitive in T20s - less time to collapse",
            },
            {
                "factor": "SCG Smaller Ground",
                "impact": 10,
                "description": "Smaller boundaries could help Pakistan's power hitters",
            },
            {
                "factor": "Australia T20 Depth",
                "impact": -25,
                "description": "Australia's T20 squad is packed with BBL and IPL experience",
            },
            {
                "factor": "Tour Fatigue & Demoralization",
                "impact": -15,
                "description": "By this point Pakistan will be mentally drained from Test losses",
            },
        ],
    },
    {
        "id": "um6",
        "date": "2027-02-12",
        "opponent": "England",
        "opponent_flag": "🏴",
        "format": "Test",
        "venue": "Rawalpindi Cricket Stadium",
        "series": "England Tour of Pakistan 2027",
        "factors": [
            {
                "factor": "Home Advantage",
                "impact": 20,
                "description": "Playing at home should help - but it hasn't always",
            },
            {
                "factor": "Bazball Effect",
                "impact": -30,
                "description": "England's aggressive approach dismantled Pakistan at home in 2022",
            },
            {
                "factor": "Flat Rawalpindi Roads",
                "impact": -15,
                "description": "Rawalpindi pitches historically produce draws or give batsmen too much",
            },
            {
                "factor": "Home Crowd Turns Hostile",
                "impact": -10,
                "description": "Pakistani fans turn on the team fast when things go wrong",
            },
        ],
    },
    {
        "id": "um7",
        "date": "2027-06-15",
        "opponent": "Zimbabwe",
        "opponent_flag": "🇿🇼",
        "format": "ODI",
        "venue": "Harare Sports Club",
        "series": "Zimbabwe Tour 2027",
        "factors": [
            {
                "factor": "Pakistan Should Win This",
                "impact": 25,
                "description": "On paper, Pakistan are far superior to Zimbabwe",
            },
            {
                "factor": "Upset Potential",
                "impact": -20,
                "description": "Pakistan lose to minnows when least expected",
            },
            {
                "factor": "Harare Conditions",
                "impact": -10,
                "description": "Zimbabwe's home conditions can be tricky for touring sides",
            },
            {
                "factor": "Complacency Factor",
                "impact": -15,
                "description": "Pakistan's biggest enemy against weaker teams is themselves",
            },
        ],
    },
]
