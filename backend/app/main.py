"""
Pakistan Cricket Hate Watch - FastAPI Backend
=============================================
The statistical brain behind the misery.

This serves all the data and runs the in-house engines:
- Loss Probability Engine (Bayesian model)
- Fraud Detection Engine (player performance scoring)
- Collapse Alert Projections (pattern matching)
"""

from dotenv import load_dotenv
load_dotenv()  # Load .env before anything reads os.getenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import defeats, matches, probability, fraud, misery, collapse, shame, scorecard

app = FastAPI(
    title="Pakistan Cricket Hate Watch API",
    description="Statistical engines and data for tracking Pakistan cricket's finest moments of despair",
    version="1.0.0",
)

# Allow Next.js frontend (dev on port 3000) to call us
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://pakistan-hate-watch.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all route groups
app.include_router(defeats.router, prefix="/api/defeats", tags=["Defeats"])
app.include_router(matches.router, prefix="/api/matches", tags=["Matches"])
app.include_router(probability.router, prefix="/api/probability", tags=["Probability Engine"])
app.include_router(fraud.router, prefix="/api/fraud", tags=["Fraud Watch"])
app.include_router(misery.router, prefix="/api/misery", tags=["Misery Dashboard"])
app.include_router(collapse.router, prefix="/api/collapse", tags=["Collapse Alerts"])
app.include_router(shame.router, prefix="/api/shame", tags=["Shame Gallery"])
app.include_router(scorecard.router, prefix="/api/scorecard", tags=["Scorecard"])


@app.get("/")
def root():
    return {
        "name": "Pakistan Cricket Hate Watch API",
        "status": "operational",
        "motto": "Tracking disappointment since 1952",
        "endpoints": {
            "defeats": "/api/defeats",
            "matches": "/api/matches",
            "probability": "/api/probability",
            "fraud": "/api/fraud",
            "misery": "/api/misery",
            "collapse": "/api/collapse",
            "shame": "/api/shame",
            "docs": "/docs",
        },
    }
