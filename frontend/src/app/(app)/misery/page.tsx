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
  Info,
} from "lucide-react";

/* eslint-disable @typescript-eslint/no-explicit-any */

export default function MiseryPage() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMiseryStats()
      .then(setStats)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-4 max-w-6xl">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="rounded-xl bg-bg-card border border-border p-6 h-40 animate-pulse" />
        ))}
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="rounded-xl bg-bg-card border border-border p-12 text-center max-w-6xl">
        <AlertTriangle className="h-8 w-8 text-accent-orange mx-auto mb-3" />
        <p className="text-sm text-text-muted">
          Backend not running. Start it with: cd backend && uvicorn app.main:app --reload
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl space-y-6">
      {/* Top Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <BigStat
          icon={<Skull className="h-6 w-6 text-accent-red" />}
          value={stats.total_defeats_tracked}
          label="Defeats Tracked"
          color="text-accent-red"
        />
        <BigStat
          icon={<Trophy className="h-6 w-6 text-accent-orange" />}
          value={stats.total_tournament_exits}
          label="Tournament Exits"
          color="text-accent-orange"
        />
        <BigStat
          icon={<Flame className="h-6 w-6 text-accent-yellow" />}
          value={stats.humiliation_index}
          label="Humiliation Index"
          color="text-accent-yellow"
        />
        <BigStat
          icon={<TrendingDown className="h-6 w-6 text-accent-purple" />}
          value={stats.average_misery_rating}
          label="Avg Misery Rating"
          color="text-accent-purple"
        />
      </div>

      {/* Severity Breakdown */}
      <div className="rounded-xl bg-bg-card border border-border p-6">
        <h3 className="text-sm font-bold mb-4 flex items-center gap-2">
          <BarChart3 className="h-4 w-4 text-pak-green" />
          Defeat Severity Breakdown
        </h3>
        <div className="space-y-3">
          <SeverityBar
            label="HUMILIATING"
            count={stats.severity_breakdown.humiliating}
            total={stats.total_defeats_tracked}
            color="bg-severity-humiliating"
          />
          <SeverityBar
            label="PAINFUL"
            count={stats.severity_breakdown.painful}
            total={stats.total_defeats_tracked}
            color="bg-severity-painful"
          />
          <SeverityBar
            label="EMBARRASSING"
            count={stats.severity_breakdown.embarrassing}
            total={stats.total_defeats_tracked}
            color="bg-severity-embarrassing"
          />
          <SeverityBar
            label="EXPECTED"
            count={stats.severity_breakdown.expected}
            total={stats.total_defeats_tracked}
            color="bg-severity-expected"
          />
        </div>
      </div>

      {/* Format Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-xl bg-bg-card border border-border p-6">
          <h3 className="text-sm font-bold mb-4">Defeats by Format</h3>
          <div className="space-y-3">
            {Object.entries(stats.format_breakdown || {}).map(([format, count]: any) => (
              <div key={format} className="flex items-center justify-between">
                <span className="text-sm text-text-secondary">{format}</span>
                <div className="flex items-center gap-2">
                  <div className="w-32 h-2 bg-bg-secondary rounded-full overflow-hidden">
                    <div
                      className="h-full bg-accent-blue rounded-full"
                      style={{
                        width: `${(count / stats.total_defeats_tracked) * 100}%`,
                      }}
                    />
                  </div>
                  <span className="text-sm font-mono font-bold text-text-primary w-6 text-right">
                    {count}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-xl bg-bg-card border border-border p-6">
          <h3 className="text-sm font-bold mb-4">Defeats by Opponent</h3>
          <div className="space-y-3">
            {stats.defeats_by_opponent?.map((o: any) => (
              <div key={o.opponent} className="flex items-center justify-between">
                <span className="text-sm text-text-secondary">{o.opponent}</span>
                <div className="flex items-center gap-2">
                  <div className="w-32 h-2 bg-bg-secondary rounded-full overflow-hidden">
                    <div
                      className="h-full bg-accent-red rounded-full"
                      style={{
                        width: `${(o.defeats / stats.total_defeats_tracked) * 100}%`,
                      }}
                    />
                  </div>
                  <span className="text-sm font-mono font-bold text-text-primary w-6 text-right">
                    {o.defeats}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Lowest Points */}
      <div className="rounded-xl bg-bg-card border border-border p-6">
        <h3 className="text-sm font-bold mb-4 flex items-center gap-2">
          <TrendingDown className="h-4 w-4 text-accent-red" />
          All-Time Lowest Points
        </h3>
        <div className="space-y-2">
          {stats.lowest_points?.map((p: any, i: number) => (
            <div
              key={i}
              className="flex items-center justify-between rounded-lg bg-bg-secondary p-3"
            >
              <div className="flex items-center gap-3">
                <span className="text-lg font-bold font-mono text-accent-red">
                  #{i + 1}
                </span>
                <span className="text-sm text-text-secondary">{p.event}</span>
              </div>
              <div className="flex items-center gap-1">
                <span className="text-xs text-text-muted">Misery</span>
                <span className="text-sm font-bold font-mono text-accent-red">
                  {p.misery}/10
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Fun Facts */}
      <div className="rounded-xl bg-bg-card border border-border p-6">
        <h3 className="text-sm font-bold mb-4 flex items-center gap-2">
          <Info className="h-4 w-4 text-pak-green" />
          Pain Facts
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {stats.fun_facts?.map((f: string, i: number) => (
            <div key={i} className="flex items-start gap-2 text-sm text-text-secondary">
              <span className="text-pak-green shrink-0">•</span>
              <span>{f}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function BigStat({
  icon,
  value,
  label,
  color,
}: {
  icon: React.ReactNode;
  value: number | string;
  label: string;
  color: string;
}) {
  return (
    <div className="rounded-xl bg-bg-card border border-border p-5">
      <div className="flex items-center justify-between mb-3">{icon}</div>
      <div className={`text-3xl font-bold font-mono ${color}`}>{value}</div>
      <div className="text-xs text-text-muted mt-1">{label}</div>
    </div>
  );
}

function SeverityBar({
  label,
  count,
  total,
  color,
}: {
  label: string;
  count: number;
  total: number;
  color: string;
}) {
  const pct = total > 0 ? (count / total) * 100 : 0;
  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs font-medium text-text-secondary">{label}</span>
        <span className="text-xs font-mono text-text-muted">
          {count} ({pct.toFixed(0)}%)
        </span>
      </div>
      <div className="w-full h-3 bg-bg-secondary rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
