# 🏏 Pakistan Cricket Hate Watch

Tracking Pakistan cricket's defeats, collapses, and disappointments with statistical precision.

A full-stack web app with a **Python FastAPI backend** powering in-house statistical engines and a **Next.js React frontend** for the UI.

## Features

| Page | Description |
|------|-------------|
| **Command Center** | Recent defeats with severity ratings, tournament exits, upcoming matches with computed loss probabilities. Matches with >60% loss probability are marked as 🔥 HATE WATCH |
| **Loss Probability Calculator** | Real-time calculator — input the current match state and get Pakistan's loss probability, alert level (MELTDOWN → STABLE), collapse risk, and projected score |
| **Collapse Alerts** | Detects and projects batting collapses using statistical pattern matching. Includes preset scenarios and a library of Pakistan's 5 classic collapse patterns |
| **Misery Dashboard** | Aggregated stats — severity breakdown, defeats by opponent/format, humiliation index, all-time lowest points, and pain facts |
| **Fraud Watch** | Player fraud detection engine. Each player gets a computed fraud score based on big-match index, decline trajectory, consistency, top-team performance, and clutch factor |
| **Shame Gallery** | Curated YouTube videos of Pakistan's most memorable defeats. Filterable by category (collapse, choke, upset-loss, all-time-low, etc.) with embedded players |

## Architecture

```
Pakistan_Hate_Watch/
├── backend/                 # Python FastAPI — the statistical brain
│   ├── app/
│   │   ├── main.py          # FastAPI entry point
│   │   ├── engines/         # In-house statistical engines
│   │   │   ├── probability_engine.py   # Bayesian loss probability (pre-match + live)
│   │   │   ├── fraud_engine.py         # Player fraud detection scoring
│   │   │   └── collapse_engine.py      # Collapse detection & projection
│   │   ├── data/            # Match data, player profiles, shame gallery
│   │   └── routers/         # API route handlers
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                # Next.js React — the presentation layer
│   ├── src/
│   │   ├── app/             # Pages (home, probability, collapse, misery, fraud, shame)
│   │   ├── components/      # Sidebar, Header
│   │   └── lib/api.ts       # API client connecting to Python backend
│   └── package.json
└── README.md
```

## In-House Engines

### Loss Probability Engine (`probability_engine.py`)
- **Pre-match mode**: Weighted factor model (venue, opponent strength, Pakistan Chaos Factor™)
- **Live match mode**: DLS-inspired resource model + Pakistan-specific collapse patterns + momentum analysis
- Accounts for Pakistan's fat-tailed probability distributions (higher chance of extreme outcomes)

### Fraud Detection Engine (`fraud_engine.py`)
- **Big Match Index (30%)**: ICC event performance vs bilaterals
- **Decline Trajectory (20%)**: Linear regression on recent performance periods
- **Consistency Score (15%)**: Variance analysis + duck rate
- **Top Team Performance (20%)**: Average vs ICC top 5 teams
- **Clutch Factor (15%)**: Chase performance and pressure situations

### Collapse Alert Engine (`collapse_engine.py`)
- Detects wicket clustering, run rate cratering, and chase chokes
- Matches against 5 historical Pakistan collapse patterns
- Projects final score under collapse conditions

## Quick Start

### 1. Start the Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API is now live at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

### 2. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

## Deployment

### Frontend → Vercel (free)
1. Push to GitHub
2. Import repo in [Vercel](https://vercel.com)
3. Set root directory to `frontend`
4. Add env var: `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`

### Backend → Render (free)
1. Create a new Web Service on [Render](https://render.com)
2. Point to this repo, set root directory to `backend`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /api/defeats/recent` | GET | Recent defeats with severity filters |
| `GET /api/defeats/tournament-exits` | GET | Tournament exit history |
| `GET /api/matches/upcoming` | GET | Upcoming matches with computed loss probabilities |
| `POST /api/probability/calculate` | POST | Real-time loss probability from match state |
| `GET /api/fraud/players` | GET | All player fraud profiles with computed scores |
| `GET /api/misery/stats` | GET | Aggregated misery statistics |
| `POST /api/collapse/detect` | POST | Collapse detection from match state |
| `GET /api/collapse/patterns` | GET | Known Pakistan collapse patterns |
| `GET /api/shame/videos` | GET | Shame gallery YouTube videos |

## Tech Stack

- **Backend**: Python 3.12, FastAPI, NumPy, Pandas, SciPy
- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS 4, Lucide Icons
- **Deployment**: Vercel (frontend), Render (backend)

---

*"Pakistan cricket: where hope goes to die and stats go to cry."* 🏏
