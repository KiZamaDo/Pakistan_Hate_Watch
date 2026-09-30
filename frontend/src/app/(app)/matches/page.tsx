"use client";

import { useEffect, useState, useCallback } from "react";
import { getAllMatches, getLiveMatches, getCricbuzzMatches } from "@/lib/api";
import Link from "next/link";
import {
  Radio,
  MapPin,
  Calendar,
  RefreshCw,
  Trophy,
  Skull,
  ArrowRight,
  ChevronRight,
  PartyPopper,
  TrendingDown,
  Flame,
} from "lucide-react";

/* eslint-disable @typescript-eslint/no-explicit-any */

const QUOTES = [
  "Inshallah boys played well",
  "Ye kudrat ka nizam hai",
  "Bhai maro mujhe maro... waqt badal diya jazbaat badal diye",
  "Ye dukh kaahe khatam nahi hota be",
  "I don't know the exact rule, I stop the ball I out, I don't stop the ball I out",
  "Hum sab clap karenge aapke liye",
  "Yes is a two",
  "Zara si ball idhar udhar hui, chuttad phatt gye",
  "Chaand pe jaake jhanda lagana aur jhande pe chaand lagana — fark hai",
];

const MEME_TAGS = [
  "🎪 Circus mode", "🤡 Clown fiesta", "💀 RIP", "🧊 Choke alert",
  "📉 Stocks crashing", "🪦 Another one", "🎭 Drama Inc.", "🔥 Dumpster fire",
  "🫠 Melting", "🦆 Duck season", "🏳️ Surrender mode", "🎰 Gamble",
];

function didPakLose(m: any): boolean | null {
  const s = (m.status_text || "").toLowerCase();
  if (!s.includes("won")) return null;
  if (s.includes("pakistan won") || s.includes("pak won")) return false;
  return true;
}

export default function MatchesPage() {
  const [matches, setMatches] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [mode, setMode] = useState<"choose" | "win" | "learn">("choose");
  const [quoteIdx, setQuoteIdx] = useState(0);

  useEffect(() => {
    setQuoteIdx(Math.floor(Math.random() * QUOTES.length));
  }, []);

  const fetchMatches = useCallback(async () => {
    setLoading(true);
    try {
      const [liveData, allData, cbData] = await Promise.all([
        getLiveMatches().catch(() => ({ matches: [] })),
        getAllMatches().catch(() => ({ matches: [] })),
        getCricbuzzMatches().catch(() => ({ matches: [] })),
      ]);
      const live: any[] = (liveData as any).matches || [];
      const all: any[] = (allData as any).matches || [];
      const cb: any[] = ((cbData as any).matches || []).map((m: any) => ({
        id: `cb_${m.id}`, name: m.name || "", status: m.status || "upcoming",
        match_type: "", venue: "", date: "",
        team1: m.teams?.[0] || "", team2: m.teams?.[1] || "",
        team1_img: "", team2_img: "", scores: [], status_text: m.name || "", source: "cricbuzz",
      }));
      const seen = new Set<string>();
      const merged: any[] = [];
      for (const m of [...live, ...all]) { if (m.id && !seen.has(m.id)) { seen.add(m.id); merged.push(m); } }
      for (const m of cb) {
        const w = m.name.toLowerCase().split(/\s+/);
        if (!merged.some((e) => w.filter((x: string) => x.length > 3 && (e.name || "").toLowerCase().includes(x)).length >= 2)) merged.push(m);
      }
      merged.sort((a, b) => {
        if (a.status === "live" && b.status !== "live") return -1;
        if (b.status === "live" && a.status !== "live") return 1;
        return (b.date || "").localeCompare(a.date || "");
      });
      setMatches(merged);
    } catch { /* */ } finally { setLoading(false); }
  }, []);

  useEffect(() => { fetchMatches(); }, [fetchMatches]);

  const liveMatches = matches.filter((m) => m.status === "live");
  const upcoming = matches.filter((m) => m.status === "upcoming");
  const completed = matches.filter((m) => m.status === "completed");
  const losses = completed.filter((m) => didPakLose(m) === true);
  const wins = completed.filter((m) => didPakLose(m) === false);
  const q = QUOTES[quoteIdx];

  return (
    <div className="max-w-5xl">
      {/* ─── LIVE TICKER ─── */}
      {liveMatches.length > 0 && (
        <div className="mb-6">
          {liveMatches.map((m) => (
            <Link key={m.id} href={`/match/${m.id}`}
              className="flex items-center gap-4 rounded-2xl border-2 border-status-live/40 bg-status-live/5 px-5 py-4 glow-red group hover:border-status-live transition-all">
              <span className="h-3 w-3 rounded-full bg-status-live animate-live shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="text-[10px] font-black text-status-live tracking-widest mb-1">LIVE — MELTDOWN WATCH</div>
                <div className="text-sm font-bold text-text-primary truncate">{m.name}</div>
                {m.scores?.length > 0 && (
                  <div className="flex flex-wrap gap-x-4 mt-1">
                    {m.scores.map((s: any, i: number) => (
                      <span key={i} className={`text-xs font-mono ${(s.inning||"").toLowerCase().includes("pakistan") ? "text-pak-green font-bold" : "text-text-muted"}`}>
                        {s.inning}: {s.runs}/{s.wickets} ({s.overs})
                      </span>
                    ))}
                  </div>
                )}
              </div>
              <ChevronRight className="h-5 w-5 text-status-live shrink-0 group-hover:translate-x-1 transition-transform" />
            </Link>
          ))}
        </div>
      )}

      {/* ─── QUOTE MARQUEE ─── */}
      <div className="text-center mb-6 py-3 border-y border-border/30">
        <p className="text-sm text-text-secondary italic">&ldquo;{q}&rdquo;</p>
      </div>

      {/* ─── THE SPLIT CHOICE ─── */}
      {mode === "choose" && (
        <div className="relative">
          {/* Split layout */}
          <div className="grid grid-cols-1 md:grid-cols-2 min-h-[380px] rounded-2xl overflow-hidden border border-border">
            {/* LEFT — Ya to Win */}
            <button onClick={() => setMode("win")}
              className="relative p-8 md:p-10 text-left bg-bg-secondary group hover:bg-pak-green/5 transition-all border-b md:border-b-0 md:border-r border-border overflow-hidden">
              <div className="absolute -right-8 -bottom-8 text-[120px] leading-none opacity-[0.04] group-hover:opacity-[0.08] transition-opacity select-none">🤞</div>
              <div className="relative z-10">
                <span className="text-xs font-bold text-pak-green bg-pak-green/10 px-3 py-1 rounded-full">UPCOMING</span>
                <h2 className="text-3xl md:text-4xl font-black text-text-primary mt-4 mb-2 leading-none">
                  Ya to<br /><span className="text-pak-green">Win</span> hai
                </h2>
                <p className="text-sm text-text-muted mb-5 max-w-[280px]">
                  Upcoming fixtures with calculated loss probability. Spoiler: it&apos;s always high.
                </p>
                <div className="text-xs text-text-muted mb-4">{upcoming.length} upcoming · {wins.length} boring wins</div>
                <span className="inline-flex items-center gap-2 text-sm font-bold text-pak-green group-hover:gap-3 transition-all">
                  Enter <ArrowRight className="h-4 w-4" />
                </span>
              </div>
            </button>

            {/* RIGHT — Ya to Learn */}
            <button onClick={() => setMode("learn")}
              className="relative p-8 md:p-10 text-left bg-bg-secondary group hover:bg-accent-red/5 transition-all overflow-hidden">
              <div className="absolute -right-8 -bottom-8 text-[120px] leading-none opacity-[0.04] group-hover:opacity-[0.08] transition-opacity select-none">💀</div>
              <div className="relative z-10">
                <span className="text-xs font-bold text-accent-red bg-accent-red/10 px-3 py-1 rounded-full">RESULTS</span>
                <h2 className="text-3xl md:text-4xl font-black text-text-primary mt-4 mb-2 leading-none">
                  Ya to<br /><span className="text-accent-red">Learn</span> hai
                </h2>
                <p className="text-sm text-text-muted mb-5 max-w-[280px]">
                  Recent results with full scorecards. Mostly defeats. Obviously.
                </p>
                <div className="text-xs text-text-muted mb-4">{losses.length} defeats · {completed.length} total completed</div>
                <span className="inline-flex items-center gap-2 text-sm font-bold text-accent-red group-hover:gap-3 transition-all">
                  Enter <ArrowRight className="h-4 w-4" />
                </span>
              </div>
            </button>
          </div>

          {/* VS divider (desktop) */}
          <div className="hidden md:flex absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-10 h-14 w-14 rounded-full bg-bg-primary border-2 border-border items-center justify-center">
            <span className="text-lg font-black text-text-muted">VS</span>
          </div>
        </div>
      )}

      {/* ─── YA TO WIN HAI ─── */}
      {mode === "win" && (
        <div>
          <div className="flex items-center justify-between mb-5">
            <button onClick={() => setMode("choose")} className="text-sm text-pak-green hover:underline flex items-center gap-1">← Back</button>
            <button onClick={fetchMatches} disabled={loading}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs text-text-muted bg-bg-card border border-border">
              <RefreshCw className={`h-3 w-3 ${loading ? "animate-spin" : ""}`} /> Refresh
            </button>
          </div>

          <div className="mb-6">
            <h2 className="text-2xl font-black text-pak-green">🤞 Ya to Win hai</h2>
            <p className="text-xs text-text-muted mt-1">Dream on. Here&apos;s the data on why you shouldn&apos;t.</p>
          </div>

          {upcoming.length === 0 && !loading ? (
            <div className="text-center py-16 text-text-muted">
              <div className="text-5xl mb-4">🏖️</div>
              <p className="font-medium">No upcoming matches</p>
              <p className="text-xs mt-1">The world gets a break</p>
            </div>
          ) : (
            /* ─── TABLE STYLE, not cards ─── */
            <div className="rounded-xl border border-border overflow-hidden">
              {/* Header */}
              <div className="grid grid-cols-[1fr_100px_120px] md:grid-cols-[1fr_140px_100px_150px] bg-bg-secondary px-4 py-2.5 border-b border-border text-[10px] font-bold text-text-muted uppercase tracking-wider">
                <div>Match</div>
                <div className="hidden md:block">Date</div>
                <div className="text-center">Loss %</div>
                <div className="text-right">Verdict</div>
              </div>
              {/* Rows */}
              {upcoming.map((m, i) => {
                const lp = m.loss_probability;
                const lossPct = lp?.loss_probability || 50;
                const verdict = lp?.verdict || "🎲 Unknown";
                const meme = MEME_TAGS[(i * 7 + 3) % MEME_TAGS.length];
                return (
                  <Link key={m.id} href={`/match/${m.id}`}
                    className={`grid grid-cols-[1fr_100px_120px] md:grid-cols-[1fr_140px_100px_150px] items-center px-4 py-3 border-b border-border/40 hover:bg-pak-green/5 transition-all group ${i % 2 === 0 ? "bg-bg-card" : "bg-bg-secondary/30"}`}>
                    {/* Match info */}
                    <div className="min-w-0 pr-3">
                      <div className="flex items-center gap-2 mb-0.5">
                        {m.match_type && <span className="text-[9px] font-bold bg-pak-green-dim text-pak-green px-1.5 py-0.5 rounded shrink-0">{m.match_type}</span>}
                        <span className="text-sm font-bold text-text-primary truncate group-hover:text-pak-green transition-colors">{m.name}</span>
                      </div>
                      <div className="flex items-center gap-2 text-[10px] text-text-muted">
                        {m.venue && <span className="flex items-center gap-0.5 truncate"><MapPin className="h-2.5 w-2.5 shrink-0" />{m.venue}</span>}
                        <span className="text-accent-orange italic hidden sm:inline">{meme}</span>
                      </div>
                    </div>
                    {/* Date */}
                    <div className="hidden md:block text-xs text-text-muted">{m.date || "TBD"}</div>
                    {/* Loss % — big, colored */}
                    <div className="text-center">
                      <span className={`text-lg font-black font-mono ${
                        lossPct >= 70 ? "text-accent-red" : lossPct >= 50 ? "text-accent-orange" : lossPct >= 35 ? "text-accent-yellow" : "text-pak-green"
                      }`}>{lossPct}%</span>
                    </div>
                    {/* Verdict */}
                    <div className="text-right text-[10px] text-text-muted leading-tight">{verdict}</div>
                  </Link>
                );
              })}
            </div>
          )}

          {/* Quote between sections */}
          {upcoming.length > 0 && (
            <div className="text-center py-4">
              <p className="text-xs text-text-muted italic">&ldquo;{QUOTES[(quoteIdx + 4) % QUOTES.length]}&rdquo;</p>
            </div>
          )}

          {/* Boring wins, collapsed */}
          {wins.length > 0 && (
            <details className="mt-4">
              <summary className="text-xs text-text-muted cursor-pointer hover:text-text-secondary">
                😴 {wins.length} boring win{wins.length > 1 ? "s" : ""} nobody asked for
              </summary>
              <div className="mt-2 space-y-1 opacity-40">
                {wins.map((m) => (
                  <Link key={m.id} href={`/match/${m.id}`} className="block text-xs text-text-muted py-1.5 px-3 rounded hover:bg-bg-card">
                    {m.name} — {m.status_text}
                  </Link>
                ))}
              </div>
            </details>
          )}
        </div>
      )}

      {/* ─── YA TO LEARN HAI ─── */}
      {mode === "learn" && (
        <div>
          <div className="flex items-center justify-between mb-5">
            <button onClick={() => setMode("choose")} className="text-sm text-accent-red hover:underline flex items-center gap-1">← Back</button>
            <button onClick={fetchMatches} disabled={loading}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs text-text-muted bg-bg-card border border-border">
              <RefreshCw className={`h-3 w-3 ${loading ? "animate-spin" : ""}`} /> Refresh
            </button>
          </div>

          <div className="mb-6">
            <h2 className="text-2xl font-black text-accent-red">📚 Ya to Learn hai</h2>
            <p className="text-xs text-text-muted mt-1">Spoiler: They never learn. Click any match for the full scorecard.</p>
          </div>

          {losses.length === 0 && !loading ? (
            <div className="text-center py-16 text-text-muted">
              <div className="text-5xl mb-4">🤯</div>
              <p className="font-medium">No recent losses?!</p>
              <p className="text-xs mt-1">Something is broken. Pakistan ALWAYS has recent losses.</p>
            </div>
          ) : (
            <div className="space-y-1">
              {losses.map((match, i) => {
                const scores = match.scores || [];
                const meme = MEME_TAGS[(i * 5 + 2) % MEME_TAGS.length];
                return (
                  <div key={match.id}>
                    <Link href={`/match/${match.id}`}
                      className="block rounded-xl border border-pak-green/20 bg-gradient-to-r from-pak-green/[0.06] to-transparent p-4 hover:from-pak-green/[0.12] transition-all group">
                      {/* Row 1: celebration + name */}
                      <div className="flex items-start justify-between gap-3 mb-2">
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <PartyPopper className="h-3.5 w-3.5 text-pak-green shrink-0" />
                            <span className="text-[10px] font-black text-pak-green">🎉 PAKISTAN LOST</span>
                            {match.match_type && (
                              <span className="text-[9px] font-bold bg-pak-green-dim text-pak-green px-1.5 py-0.5 rounded">{match.match_type}</span>
                            )}
                            <span className="text-[10px] text-accent-orange italic hidden sm:inline">{meme}</span>
                          </div>
                          <h3 className="text-sm font-bold text-text-primary group-hover:text-pak-green transition-colors truncate">{match.name}</h3>
                        </div>
                        <ChevronRight className="h-4 w-4 text-pak-green shrink-0 mt-1 opacity-0 group-hover:opacity-100 transition-opacity" />
                      </div>

                      {/* Row 2: inline scores */}
                      {scores.length > 0 && (
                        <div className="flex flex-wrap gap-x-4 gap-y-0.5 mb-2">
                          {scores.map((s: any, j: number) => {
                            const isPak = (s.inning || "").toLowerCase().includes("pakistan");
                            return (
                              <span key={j} className={`text-xs font-mono ${isPak ? "text-pak-green font-bold" : "text-text-muted"}`}>
                                {s.inning}: <strong>{s.runs}/{s.wickets}</strong> ({s.overs})
                              </span>
                            );
                          })}
                        </div>
                      )}

                      {/* Row 3: result + meta */}
                      <div className="flex flex-wrap items-center gap-3 text-[10px] text-text-muted">
                        <span className="text-pak-green font-medium">🎉 {match.status_text}</span>
                        {match.venue && <span className="flex items-center gap-0.5"><MapPin className="h-2.5 w-2.5" />{match.venue}</span>}
                        {match.date && <span className="flex items-center gap-0.5"><Calendar className="h-2.5 w-2.5" />{match.date}</span>}
                      </div>
                    </Link>

                    {/* Sprinkle quotes */}
                    {i % 3 === 1 && i < losses.length - 1 && (
                      <div className="text-center py-2.5">
                        <p className="text-[11px] text-text-muted italic">&ldquo;{QUOTES[(i + 5) % QUOTES.length]}&rdquo;</p>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}

          {/* Other completed */}
          {completed.length > losses.length && (
            <details className="mt-6">
              <summary className="text-xs text-text-muted cursor-pointer hover:text-text-secondary">
                😴 {completed.length - losses.length} other result{completed.length - losses.length > 1 ? "s" : ""} (wins, draws, abandoned)
              </summary>
              <div className="mt-2 space-y-1 opacity-40">
                {completed.filter(m => didPakLose(m) !== true).map((m) => (
                  <Link key={m.id} href={`/match/${m.id}`} className="block text-xs text-text-muted py-1.5 px-3 rounded hover:bg-bg-card">
                    {m.name} — {m.status_text}
                  </Link>
                ))}
              </div>
            </details>
          )}
        </div>
      )}

      {/* Loading */}
      {loading && mode !== "choose" && (
        <div className="space-y-3 mt-4">{[1,2,3].map((i) => (<div key={i} className="h-16 rounded-xl bg-bg-card border border-border animate-pulse" />))}</div>
      )}
    </div>
  );
}
