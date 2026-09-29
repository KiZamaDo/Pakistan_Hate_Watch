"use client";

import { useEffect, useState, useCallback } from "react";
import { getAllMatches, getLiveMatches, getCricbuzzMatches } from "@/lib/api";
import Link from "next/link";
import {
  Radio,
  Clock,
  Calendar,
  List,
  MapPin,
  AlertTriangle,
  RefreshCw,
  PartyPopper,
} from "lucide-react";

/* eslint-disable @typescript-eslint/no-explicit-any */

type TabKey = "all" | "live" | "completed" | "upcoming";

const tabs: { key: TabKey; label: string; icon: React.ReactNode }[] = [
  { key: "all", label: "All", icon: <List className="h-4 w-4" /> },
  { key: "live", label: "Live", icon: <Radio className="h-4 w-4" /> },
  { key: "completed", label: "Recent", icon: <Clock className="h-4 w-4" /> },
  { key: "upcoming", label: "Upcoming", icon: <Calendar className="h-4 w-4" /> },
];

function didPakLose(match: any): boolean | null {
  const s = (match.status_text || "").toLowerCase();
  if (!s.includes("won")) return null;
  if (s.includes("pakistan won") || s.includes("pak won")) return false;
  return true;
}

export default function HomePage() {
  const [matches, setMatches] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState<TabKey>("all");

  const fetchMatches = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [liveData, allData, cbData] = await Promise.all([
        getLiveMatches().catch(() => ({ matches: [] })),
        getAllMatches().catch(() => ({ matches: [] })),
        getCricbuzzMatches().catch(() => ({ matches: [], all_matches: [] })),
      ]);

      const liveMatches: any[] = (liveData as any).matches || [];
      const allMatches: any[] = (allData as any).matches || [];
      const cbPakMatches: any[] = (cbData as any).matches || [];

      const cbNormalized = cbPakMatches.map((m: any) => ({
        id: `cb_${m.id}`,
        cricbuzz_id: m.id,
        name: m.name || m.title || "",
        status: m.status || "upcoming",
        match_type: "",
        venue: "",
        date: "",
        team1: m.teams?.[0] || "",
        team2: m.teams?.[1] || "",
        team1_img: "",
        team2_img: "",
        scores: [],
        status_text: m.name || "",
        series: "",
        source: "cricbuzz",
      }));

      const seen = new Set<string>();
      const merged: any[] = [];
      for (const m of liveMatches) {
        if (m.id && !seen.has(m.id)) { seen.add(m.id); merged.push({ ...m, source: "cricapi" }); }
      }
      for (const m of allMatches) {
        if (m.id && !seen.has(m.id)) { seen.add(m.id); merged.push({ ...m, source: "cricapi" }); }
      }
      for (const m of cbNormalized) {
        const words = m.name.toLowerCase().split(/\s+/);
        const dup = merged.some((ex) => {
          const ew = (ex.name || "").toLowerCase();
          return words.filter((w: string) => w.length > 3 && ew.includes(w)).length >= 2;
        });
        if (!dup) merged.push(m);
      }
      merged.sort((a, b) => {
        if (a.status === "live" && b.status !== "live") return -1;
        if (b.status === "live" && a.status !== "live") return 1;
        return (b.date || "").localeCompare(a.date || "");
      });
      setMatches(merged);
    } catch {
      setError("Could not fetch matches. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchMatches(); }, [fetchMatches]);

  const filtered = activeTab === "all" ? matches : matches.filter((m) => m.status === activeTab);
  const liveCount = matches.filter((m) => m.status === "live").length;

  return (
    <div className="max-w-5xl space-y-6">
      {/* Tabs */}
      <div className="flex items-center gap-2 flex-wrap">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all border ${
              activeTab === tab.key
                ? "bg-pak-green-dim text-pak-green border-pak-green/30"
                : "text-text-muted hover:text-text-secondary bg-bg-card border-border hover:border-pak-green/20"
            }`}
          >
            {tab.icon}
            {tab.label}
            {tab.key === "live" && liveCount > 0 && (
              <span className="h-5 min-w-5 flex items-center justify-center rounded-full bg-status-live text-white text-xs font-bold px-1 animate-live">
                {liveCount}
              </span>
            )}
          </button>
        ))}
        <button
          onClick={fetchMatches}
          disabled={loading}
          className="ml-auto flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs text-text-muted hover:text-pak-green bg-bg-card border border-border hover:border-pak-green/20 transition-all disabled:opacity-50"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${loading ? "animate-spin" : ""}`} /> Refresh
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="rounded-xl bg-accent-orange/10 border border-accent-orange/20 p-4 text-sm text-accent-orange flex items-start gap-3">
          <AlertTriangle className="h-5 w-5 shrink-0 mt-0.5" />
          <div>
            <p className="font-medium">No live data available</p>
            <p className="text-xs mt-1 opacity-80">{error}</p>
          </div>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="rounded-xl bg-bg-card border border-border h-52 animate-pulse" />
          ))}
        </div>
      )}

      {/* Empty */}
      {!loading && filtered.length === 0 && (
        <div className="rounded-xl bg-bg-card border border-border p-12 text-center">
          <Calendar className="h-10 w-10 text-text-muted mx-auto mb-3" />
          <p className="text-text-secondary font-medium">
            {activeTab === "live" ? "No live Pakistan matches right now" :
             activeTab === "upcoming" ? "No upcoming Pakistan matches" : "No matches found"}
          </p>
        </div>
      )}

      {/* Match Grid — Boxed cards */}
      {!loading && filtered.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filtered.map((match) => (
            <MatchBox key={match.id} match={match} />
          ))}
        </div>
      )}
    </div>
  );
}

/* ========== MATCH BOX CARD ========== */

function MatchBox({ match }: { match: any }) {
  const scores = match.scores || [];
  const lost = didPakLose(match);
  const isLive = match.status === "live";
  const isUpcoming = match.status === "upcoming";

  // FESTIVE = Pakistan lost (celebrate the pain 🎉)
  // DULL = Pakistan won (boring, who cares)
  const festive = lost === true;
  const dull = lost === false;

  return (
    <Link
      href={`/match/${match.id}`}
      className={`block rounded-xl border overflow-hidden transition-all group relative ${
        festive
          ? "bg-gradient-to-br from-pak-green/20 via-bg-card to-accent-yellow/10 border-pak-green/50 hover:border-pak-green glow-green"
          : dull
          ? "bg-bg-card/50 border-border/40 opacity-50 hover:opacity-70 grayscale-[30%]"
          : isLive
          ? "bg-bg-card border-status-live/40 glow-red"
          : "bg-bg-card border-border hover:border-pak-green/30"
      }`}
    >
      {/* Top banner */}
      {festive && (
        <div className="bg-pak-green/25 border-b border-pak-green/30 px-4 py-1.5 flex items-center justify-between">
          <span className="text-[11px] font-bold text-pak-green flex items-center gap-1.5">
            <PartyPopper className="h-3.5 w-3.5" />
            🎉 PAKISTAN LOST — HATE WATCH HIGHLIGHT 🎊
          </span>
        </div>
      )}
      {dull && (
        <div className="bg-bg-secondary/40 border-b border-border/30 px-4 py-1">
          <span className="text-[10px] text-text-muted">😴 Pakistan won — nothing to see here</span>
        </div>
      )}
      {isLive && (
        <div className="bg-status-live/15 border-b border-status-live/25 px-4 py-1.5 flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-status-live animate-live" />
          <span className="text-[11px] font-bold text-status-live">LIVE — POTENTIAL MELTDOWN</span>
        </div>
      )}

      <div className="p-4 space-y-3">
        {/* Format + venue row */}
        <div className="flex items-center gap-2 text-[10px] text-text-muted">
          {match.match_type && (
            <span className="bg-pak-green-dim text-pak-green px-2 py-0.5 rounded font-semibold">
              {match.match_type}
            </span>
          )}
          {match.venue && (
            <span className="flex items-center gap-1 truncate">
              <MapPin className="h-2.5 w-2.5 shrink-0" />{match.venue}
            </span>
          )}
        </div>

        {/* Team 1 row */}
        <TeamScoreRow
          name={match.team1}
          img={match.team1_img}
          scores={scores}
          isPak={(match.team1 || "").toLowerCase().includes("pakistan")}
          festive={festive}
        />

        {/* VS divider */}
        <div className="text-center text-[10px] text-text-muted font-bold tracking-widest">VS</div>

        {/* Team 2 row */}
        <TeamScoreRow
          name={match.team2}
          img={match.team2_img}
          scores={scores}
          isPak={(match.team2 || "").toLowerCase().includes("pakistan")}
          festive={festive}
        />

        {/* Result / status */}
        {match.status_text && (
          <div className={`text-xs font-medium pt-2 border-t border-border/30 ${
            festive ? "text-pak-green" :
            dull ? "text-text-muted/60" :
            isLive ? "text-status-live animate-live" :
            "text-text-muted"
          }`}>
            {festive && "🎉 "}{match.status_text}
          </div>
        )}

        {/* Date for upcoming */}
        {isUpcoming && match.date && (
          <div className="text-[10px] text-text-muted flex items-center gap-1">
            <Calendar className="h-3 w-3" /> {match.date}
          </div>
        )}
      </div>

      {/* Hover hint */}
      <div className="absolute bottom-2 right-3 text-[10px] text-pak-green opacity-0 group-hover:opacity-100 transition-opacity">
        View scorecard →
      </div>
    </Link>
  );
}

/* ========== TEAM SCORE ROW ========== */

function TeamScoreRow({
  name, img, scores, isPak, festive,
}: {
  name: string;
  img?: string;
  scores: any[];
  isPak: boolean;
  festive: boolean;
}) {
  const teamWord = (name || "").toLowerCase().split(" ")[0];
  const teamScores = scores.filter((s: any) =>
    (s.inning || "").toLowerCase().includes(teamWord)
  );

  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2.5">
        {img ? (
          <img src={img} alt={name} className="h-8 w-8 rounded-full object-cover border border-border" />
        ) : (
          <div className={`h-8 w-8 rounded-full flex items-center justify-center text-xs font-bold border ${
            isPak
              ? "bg-pak-green-dim text-pak-green border-pak-green/30"
              : "bg-bg-secondary text-text-muted border-border"
          }`}>
            {name?.charAt(0)}
          </div>
        )}
        <span className={`text-sm font-semibold ${
          isPak ? (festive ? "text-pak-green" : "text-pak-green") : "text-text-primary"
        }`}>
          {name || "TBD"}
        </span>
      </div>

      {/* Scores — show all innings for this team */}
      {teamScores.length > 0 && (
        <div className="flex flex-col items-end gap-0.5">
          {teamScores.map((s: any, i: number) => (
            <span key={i} className="text-sm font-mono font-bold text-text-primary">
              {s.runs}/{s.wickets}
              <span className="text-text-muted font-normal text-[10px] ml-1">({s.overs})</span>
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
