# 🇵🇰 Pakistan Cricket Hate Watch

> *"Watching Pakistan lose is your guilty pleasure? Well, you are not alone."*

A full-stack web app tracking Pakistan cricket's defeats, collapses, and disappointments with statistical precision. Built with a **Python FastAPI backend** powering in-house statistical engines and a **Next.js React frontend**.

## Features

### 🏏 Matches — "Ya to Win hai... Ya to Learn hai"
- **Ya to Win hai** — Upcoming Pakistan fixtures with computed loss probability (h2h record, ICC rankings, recent form, venue factor, and a Pakistan Chaos Multiplier™)
- **Ya to Learn hai** — Recent defeats with inline scores, festive celebration styling for losses, and full scorecards via Cricbuzz scraper
- Live match tracking with meltdown alerts
- Real match data from CricketData.org API + Cricbuzz scraper for full batting/bowling scorecards
- Iconic quotes sprinkled throughout — *"Zara si ball idhar udhar hui, chuttad phatt gye"*, *"Inshallah boys played well"*, *"Yes is a two"*

### 📉 Fraud Watch — T20I Player Report Cards
Each player in the current Pakistan T20I squad gets a computed fraud score (0-100, lower = bigger fraud) based on:

| Component | Weight | What it measures |
|-----------|--------|-----------------|
| Match-Winning Ability | 30% | MOM awards vs Test nations, successful chase rate, ICC knockout avg |
| Strike Rate Analysis | 25% | T20I SR, SR vs Test nations, stat-padding gap (SR vs associates minus SR vs real teams) |
| ICC Tournament Performance | 25% | T20 WC avg/SR, powerplay SR in World Cups, knockout avg |
| Consistency & Trend | 20% | Form trajectory, big match failure rate, dropped-from-squad penalty |

Players include nicknames: Ghante Ka King (Babar Azam), Rizzu Symonds (Rizwan), Fakhar Tulla (Fakhar Zaman), Farru Ferrari (Sahibzada Farhan), Shaheen Sofa, Haris Tepia, Wide Ball (Nawaz), and more.

### 💀 Misery Dashboard — Since 2022
- **22 defeats** tracked with proper categories:
  - **Humiliating** — Lost by massive margins (innings defeats, 100+ runs, 8+ wickets)
  - **Embarrassing** — Lost to minnow/lower-ranked teams (USA, Zimbabwe, Afghanistan)
  - **Expected** — Competitive losses to higher-ranked teams
- **ICC Tournament Record** — 0 trophies from 5 events (T20 WC 2022 Final loss, ODI WC 2023 league exit, T20 WC 2024 group stage exit, Champions Trophy 2025 host knocked out, T20 WC 2026 Super 8 exit)
- **Home Series Record** — Won 2, Lost 4 since 2022
- **Head-to-Head** vs all international teams (India: 1W-10L, 8.3% win rate)

### 🎬 Shame Gallery
Curated YouTube videos of Pakistan's most memorable defeats with verified embeddable IDs:
- USA Super Over upset (T20 WC 2024)
- 114 all out vs India (T20 WC 2026)
- Wade's 3 sixes off Shaheen (T20 WC 2021 SF)
- Afghanistan chasing 283 (ODI WC 2023)
- Pakistan 49 all out vs South Africa
- And more, filterable by category

### 🚨 Collapse Alerts
Collapse detection engine with 5 documented Pakistan collapse patterns, preset simulation scenarios, and projected scores.

## Architecture

```
Pakistan_Hate_Watch/
├── backend/                    # Python FastAPI
│   ├── app/
│   │   ├── main.py             # FastAPI entry point, CORS, route mounting
│   │   ├── engines/
│   │   │   ├── probability_engine.py  # Loss probability (h2h + ranking + form + venue + chaos)
│   │   │   ├── fraud_engine.py        # T20I fraud detection (4-component scoring)
│   │   │   └── collapse_engine.py     # Collapse pattern matching & projection
│   │   ├── services/
│   │   │   ├── cricket_api.py         # CricketData.org API integration
│   │   │   └── cricbuzz_scraper.py    # Cricbuzz HTML scraper for full scorecards
│   │   ├── data/
│   │   │   ├── defeats.py            # Defeats, tournament record, h2h, home series (since 2022)
│   │   │   ├── players.py            # T20I squad fraud profiles with nicknames
│   │   │   ├── matches.py            # Upcoming match data
│   │   │   └── shame_gallery.py      # YouTube video IDs (verified embeddable)
│   │   └── routers/                   # API route handlers
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env                           # CRICKET_API_KEY (not committed)
├── frontend/                   # Next.js 16 + React 19
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx               # Landing page ("guilty pleasure")
│   │   │   └── (app)/                 # App pages with sidebar layout
│   │   │       ├── matches/           # Ya to Win / Ya to Learn
│   │   │       ├── match/[id]/        # Match detail + scorecard + loss calc + fraud alerts
│   │   │       ├── fraud/             # Fraud Watch with formula explanation
│   │   │       ├── misery/            # Misery Dashboard since 2022
│   │   │       ├── shame/             # Shame Gallery with YouTube embeds
│   │   │       └── collapse/          # Collapse Alerts
│   │   ├── components/                # Sidebar, Header
│   │   └── lib/api.ts                 # API client
│   └── package.json
├── .gitignore
└── README.md
```

## Data Sources

| Source | What it provides | Cost |
|--------|-----------------|------|
| [CricketData.org](https://cricketdata.org) | Match listings, live scores, innings totals, toss, result | Free (100 req/day) |
| Cricbuzz (scraped) | Full batting/bowling scorecards, ball-by-ball | Free (unofficial scraper) |
| In-house | Loss probability, fraud scores, collapse detection | Our own engines |

## Quick Start

### 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Get a free API key at https://cricketdata.org
echo "CRICKET_API_KEY=your-key-here" > .env

uvicorn app.main:app --reload --port 8000
```

API docs at http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

## Deployment

### Frontend → Vercel (free)
1. Push to GitHub
2. Import repo in [Vercel](https://vercel.com)
3. Set root directory to `frontend`
4. Add env var: `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`

### Backend → Render (free)
1. Create a Web Service on [Render](https://render.com)
2. Root directory: `backend`
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add env var: `CRICKET_API_KEY=your-key`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/matches/live` | GET | Live Pakistan matches from CricAPI |
| `/api/matches/all` | GET | All matches with loss probability for upcoming |
| `/api/matches/{id}/detail` | GET | Match detail + live loss calc + fraud alerts |
| `/api/scorecard/cricbuzz/{id}` | GET | Full scorecard from Cricbuzz |
| `/api/fraud/players` | GET | All player fraud profiles with computed scores |
| `/api/misery/stats` | GET | Misery dashboard stats since 2022 |
| `/api/defeats/recent` | GET | Recent defeats with category filter |
| `/api/collapse/detect` | POST | Collapse detection from match state |
| `/api/collapse/patterns` | GET | Known Pakistan collapse patterns |
| `/api/shame/videos` | GET | Shame gallery YouTube videos |

## Tech Stack

- **Backend**: Python 3.12, FastAPI, NumPy, BeautifulSoup4, httpx
- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS 4, Lucide Icons
- **Data**: CricketData.org API, Cricbuzz scraper
- **Deployment**: Vercel (frontend), Render (backend)

## Dedication

*To Wasay bhai, Iffi bhai, and Neem ka Ped — I owe you one* 🤝

---

*"Zara si ball idhar udhar hui, chuttad phatt gye"* 🏏
