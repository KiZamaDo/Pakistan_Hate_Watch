/**
 * API Client - connects to the Python FastAPI backend
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });
  if (!res.ok) {
    throw new Error(`API Error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

// --- Matches (CricAPI powered) ---

export async function getLiveMatches() {
  return fetchAPI("/api/matches/live");
}

export async function getAllMatches(status?: string) {
  const params = new URLSearchParams();
  if (status) params.set("status", status);
  const qs = params.toString();
  return fetchAPI(`/api/matches/all${qs ? `?${qs}` : ""}`);
}

export async function getMatchDetail(matchId: string) {
  return fetchAPI(`/api/matches/${matchId}/detail`);
}

// --- Scorecard (Cricbuzz scraper) ---

export async function getCricbuzzMatches() {
  return fetchAPI("/api/scorecard/cricbuzz/matches");
}

export async function getCricbuzzScorecard(cricbuzzMatchId: string) {
  return fetchAPI(`/api/scorecard/cricbuzz/${cricbuzzMatchId}`);
}

// --- Defeats (historical data) ---

export async function getRecentDefeats(limit = 10) {
  return fetchAPI(`/api/defeats/recent?limit=${limit}`);
}

export async function getTournamentExits() {
  return fetchAPI("/api/defeats/tournament-exits");
}

// --- Fraud Watch ---

export async function getFraudProfiles(rating?: string) {
  const params = new URLSearchParams();
  if (rating) params.set("rating", rating);
  const qs = params.toString();
  return fetchAPI(`/api/fraud/players${qs ? `?${qs}` : ""}`);
}

// --- Misery Dashboard ---

export async function getMiseryStats() {
  return fetchAPI("/api/misery/stats");
}

// --- Collapse ---

export interface CollapseInput {
  match_format: string;
  overs: number;
  runs: number;
  wickets: number;
  total_overs: number;
  recent_wickets: { over: number; runs_at_wicket: number }[];
  recent_run_rates: number[];
  batting_first: boolean;
  target?: number;
}

export async function detectCollapse(input: CollapseInput) {
  return fetchAPI("/api/collapse/detect", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function getCollapsePatterns() {
  return fetchAPI("/api/collapse/patterns");
}

// --- Shame Gallery ---

export async function getShameVideos(category?: string) {
  const params = new URLSearchParams();
  if (category) params.set("category", category);
  const qs = params.toString();
  return fetchAPI(`/api/shame/videos${qs ? `?${qs}` : ""}`);
}
