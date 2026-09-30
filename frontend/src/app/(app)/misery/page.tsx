"use client";

import { useEffect, useState } from "react";
import { getMiseryStats } from "@/lib/api";
import {
  BarChart3,
  TrendingDown,
  Skull,
  Trophy,
  AlertTriangle,
  Flame,
  Home,
  Shield,
  Info,
} from "lucide-react";

/* eslint-disable @typescript-eslint/no-explicit-any */

export default function MiseryPage() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMiseryStats().then(setStats).catch(() => {}).finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div className="max-w-5xl space-y-4">{[1,2,3,4].map(i => <div key={i} className="h-40 rounded-xl bg-bg-card border border-border animate-pulse" />)}</div>
  );
  if (!stats) return (
    <div className="max-w-5xl rounded-xl bg-bg-card border border-border p-12 text-center">
      <AlertTriangle className="h-8 w-8 text-accent-orange mx-auto mb-3" />
      <p className="text-sm text-text-muted">Backend not running</p>
    </div>
  );

  const cat = stats.category_breakdown || {};
  const h2h = stats.head_to_head || {};
  const tournaments = stats.tournament_record?.tournaments || [];
  const homeSeries = stats.home_series?.series || [];
  const overall = stats.overall_record || {};

  return (
    <div className="max-w-5xl space-y-8">
      {/* Period badge */}
      <div className="text-xs text-text-muted">{stats.period}</div>

      {/* ─── TOP LINE NUMBERS ─── */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <NumBlock value={stats.total_defeats} label="Total Defeats" icon={<Skull className="h-5 w-5 text-accent-red" />} />
        <NumBlock value={`${overall.win_pct || 0}%`} label="Win Rate" icon={<TrendingDown className="h-5 w-5 text-accent-orange" />} />
        <NumBlock value={stats.tournament_record?.trophies_won ?? 0} label="ICC Trophies" icon={<Trophy className="h-5 w-5 text-accent-yellow" />} />
        <NumBlock value={stats.average_misery} label="Avg Misery /10" icon={<Flame className="h-5 w-5 text-accent-red" />} />
      </div>

      {/* ─── DEFEAT CATEGORIES ─── */}
      <section>
        <h3 className="text-sm font-bold text-text-primary mb-4 flex items-center gap-2">
          <BarChart3 className="h-4 w-4 text-pak-green" /> Defeat Categories
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Humiliating */}
          <CategoryBlock
            title="💀 Humiliating"
            count={cat.humiliating?.count || 0}
            total={stats.total_defeats}
            description={cat.humiliating?.description || ""}
            matches={cat.humiliating?.matches || []}
            color="accent-red"
          />
          {/* Embarrassing */}
          <CategoryBlock
            title="🤡 Embarrassing"
            count={cat.embarrassing?.count || 0}
            total={stats.total_defeats}
            description={cat.embarrassing?.description || ""}
            matches={cat.embarrassing?.matches || []}
            color="accent-orange"
          />
          {/* Expected */}
          <CategoryBlock
            title="🤷 Expected"
            count={cat.expected?.count || 0}
            total={stats.total_defeats}
            description={cat.expected?.description || ""}
            matches={[]}
            color="text-muted"
          />
        </div>
      </section>

      {/* ─── TOURNAMENT RECORD ─── */}
      <section>
        <h3 className="text-sm font-bold text-text-primary mb-4 flex items-center gap-2">
          <Trophy className="h-4 w-4 text-accent-yellow" /> ICC Tournament Record Since 2022
        </h3>
        <div className="rounded-xl border border-border overflow-hidden">
          <div className="grid grid-cols-[1fr_140px_100px] bg-bg-secondary px-4 py-2 border-b border-border text-[10px] font-bold text-text-muted uppercase tracking-wider">
            <div>Tournament</div>
            <div>Stage Reached</div>
            <div className="text-right">Pain /10</div>
          </div>
          {tournaments.map((t: any, i: number) => (
            <div key={i} className={`grid grid-cols-[1fr_140px_100px] px-4 py-3 border-b border-border/30 ${i % 2 === 0 ? "bg-bg-card" : "bg-bg-secondary/30"}`}>
              <div className="text-sm font-medium text-text-primary">{t.tournament}</div>
              <div className="text-xs text-text-muted">{t.result}</div>
              <div className="text-right">
                <span className={`text-sm font-black font-mono ${t.embarrassment >= 9 ? "text-accent-red" : t.embarrassment >= 7 ? "text-accent-orange" : "text-text-muted"}`}>
                  {t.embarrassment}
                </span>
              </div>
            </div>
          ))}
          <div className="px-4 py-2 bg-bg-secondary text-xs text-accent-red font-bold">
            {stats.tournament_record?.summary}
          </div>
        </div>
      </section>

      {/* ─── HOME SERIES ─── */}
      <section>
        <h3 className="text-sm font-bold text-text-primary mb-4 flex items-center gap-2">
          <Home className="h-4 w-4 text-pak-green" /> Home Series Record
        </h3>
        <div className="rounded-xl border border-border overflow-hidden">
          <div className="grid grid-cols-[1fr_60px_100px_100px] bg-bg-secondary px-4 py-2 border-b border-border text-[10px] font-bold text-text-muted uppercase tracking-wider">
            <div>Opponent</div>
            <div>Year</div>
            <div>Format</div>
            <div className="text-right">Result</div>
          </div>
          {homeSeries.map((s: any, i: number) => (
            <div key={i} className={`grid grid-cols-[1fr_60px_100px_100px] px-4 py-2.5 border-b border-border/30 ${i % 2 === 0 ? "bg-bg-card" : "bg-bg-secondary/30"}`}>
              <div className="text-sm text-text-primary">{s.opponent}</div>
              <div className="text-xs text-text-muted">{s.year}</div>
              <div className="text-xs text-text-muted">{s.format}</div>
              <div className={`text-right text-xs font-bold ${s.won ? "text-pak-green" : "text-accent-red"}`}>
                {s.result}
              </div>
            </div>
          ))}
          <div className="px-4 py-2 bg-bg-secondary text-xs text-text-muted">
            {stats.home_series?.summary}
          </div>
        </div>
      </section>

      {/* ─── HEAD TO HEAD ─── */}
      <section>
        <h3 className="text-sm font-bold text-text-primary mb-4 flex items-center gap-2">
          <Shield className="h-4 w-4 text-accent-blue" /> Head-to-Head vs Test Nations (Since 2022)
        </h3>
        <div className="rounded-xl border border-border overflow-hidden">
          <div className="grid grid-cols-[1fr_50px_50px_50px_70px] bg-bg-secondary px-4 py-2 border-b border-border text-[10px] font-bold text-text-muted uppercase tracking-wider">
            <div>Opponent</div>
            <div className="text-center">P</div>
            <div className="text-center">W</div>
            <div className="text-center">L</div>
            <div className="text-right">Win %</div>
          </div>
          {Object.entries(h2h).map(([opp, rec]: [string, any], i) => (
            <div key={opp} className={`grid grid-cols-[1fr_50px_50px_50px_70px] px-4 py-2 border-b border-border/30 ${i % 2 === 0 ? "bg-bg-card" : "bg-bg-secondary/30"}`}>
              <div className="text-sm text-text-primary">{opp}</div>
              <div className="text-center text-xs text-text-muted font-mono">{rec.played}</div>
              <div className="text-center text-xs text-pak-green font-mono font-bold">{rec.won}</div>
              <div className="text-center text-xs text-accent-red font-mono font-bold">{rec.lost}</div>
              <div className="text-right">
                <span className={`text-xs font-bold font-mono ${rec.win_pct >= 50 ? "text-pak-green" : rec.win_pct >= 30 ? "text-accent-orange" : "text-accent-red"}`}>
                  {rec.win_pct}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ─── LOWLIGHTS ─── */}
      <section>
        <h3 className="text-sm font-bold text-text-primary mb-4 flex items-center gap-2">
          <TrendingDown className="h-4 w-4 text-accent-red" /> All-Time Lowlights
        </h3>
        <div className="space-y-1.5">
          {stats.lowlights?.map((l: any, i: number) => (
            <div key={i} className="flex items-center justify-between rounded-lg bg-bg-card border border-border/40 px-4 py-2.5">
              <div className="flex items-center gap-3">
                <span className="text-lg font-black font-mono text-accent-red w-6 text-right">{i + 1}</span>
                <span className="text-sm text-text-secondary">{l.event}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
                  l.category === "humiliating" ? "bg-accent-red/15 text-accent-red" :
                  l.category === "embarrassing" ? "bg-accent-orange/15 text-accent-orange" :
                  "bg-bg-secondary text-text-muted"
                }`}>{l.category}</span>
                <span className="text-sm font-bold font-mono text-accent-red">{l.misery}/10</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ─── FUN FACTS ─── */}
      <section>
        <h3 className="text-sm font-bold text-text-primary mb-4 flex items-center gap-2">
          <Info className="h-4 w-4 text-pak-green" /> Pain Facts
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {stats.fun_facts?.map((f: string, i: number) => (
            <div key={i} className="flex items-start gap-2 text-sm text-text-secondary bg-bg-card rounded-lg px-3 py-2.5 border border-border/30">
              <span className="text-pak-green shrink-0">•</span>
              <span>{f}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function NumBlock({ value, label, icon }: { value: any; label: string; icon: React.ReactNode }) {
  return (
    <div className="rounded-xl bg-bg-card border border-border p-4">
      <div className="flex items-center justify-between mb-2">{icon}</div>
      <div className="text-3xl font-black font-mono text-text-primary">{value}</div>
      <div className="text-xs text-text-muted mt-1">{label}</div>
    </div>
  );
}

function CategoryBlock({ title, count, total, description, matches, color }: {
  title: string; count: number; total: number; description: string; matches: any[]; color: string;
}) {
  const pct = total > 0 ? Math.round((count / total) * 100) : 0;
  return (
    <div className="rounded-xl bg-bg-card border border-border p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-bold">{title}</span>
        <span className={`text-2xl font-black font-mono text-${color}`}>{count}</span>
      </div>
      <div className="w-full h-1.5 bg-bg-secondary rounded-full mb-2 overflow-hidden">
        <div className={`h-full rounded-full bg-${color}`} style={{ width: `${pct}%` }} />
      </div>
      <p className="text-[10px] text-text-muted mb-2">{description}</p>
      {matches.length > 0 && (
        <div className="space-y-1 mt-2 pt-2 border-t border-border/30">
          {matches.map((m: any, i: number) => (
            <div key={i} className="text-[10px] text-text-muted">
              <span className={`text-${color} font-medium`}>vs {m.opponent}</span> — {m.margin} {m.tournament && `(${m.tournament})`}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
