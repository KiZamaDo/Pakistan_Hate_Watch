"use client";

import { useEffect, useState } from "react";
import { detectCollapse, getCollapsePatterns, type CollapseInput } from "@/lib/api";
import { AlertTriangle, Zap, BookOpen, Play, Skull } from "lucide-react";

/* eslint-disable @typescript-eslint/no-explicit-any */

const alertBadgeStyles: Record<string, string> = {
  MELTDOWN: "bg-alert-meltdown text-white glow-red",
  COLLAPSE_INCOMING: "bg-alert-collapse text-white",
  CHOKING: "bg-alert-choking text-bg-primary",
  NERVOUS: "bg-alert-nervous text-white",
  STABLE: "bg-alert-stable text-bg-primary",
};

export default function CollapsePage() {
  const [patterns, setPatterns] = useState<any>(null);
  const [simResult, setSimResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getCollapsePatterns().then(setPatterns).catch(() => {});
  }, []);

  const runSimulation = async (scenario: CollapseInput) => {
    setLoading(true);
    try {
      const result = await detectCollapse(scenario);
      setSimResult(result);
    } catch {
      // Backend not running
    } finally {
      setLoading(false);
    }
  };

  const presetScenarios: { label: string; input: CollapseInput }[] = [
    {
      label: "🔥 Classic Top-Order Implosion (45/4 in 8 overs)",
      input: {
        match_format: "ODI",
        overs: 8,
        runs: 45,
        wickets: 4,
        total_overs: 50,
        recent_wickets: [
          { over: 3.2, runs_at_wicket: 12 },
          { over: 5.1, runs_at_wicket: 22 },
          { over: 6.5, runs_at_wicket: 30 },
          { over: 7.4, runs_at_wicket: 38 },
        ],
        recent_run_rates: [6, 5, 4, 3, 4, 5, 3, 2],
        batting_first: true,
      },
    },
    {
      label: "💀 Middle-Order Meltdown (67/5 in 18 overs)",
      input: {
        match_format: "ODI",
        overs: 18.2,
        runs: 67,
        wickets: 5,
        total_overs: 50,
        recent_wickets: [
          { over: 14.1, runs_at_wicket: 52 },
          { over: 15.5, runs_at_wicket: 55 },
          { over: 17.3, runs_at_wicket: 61 },
        ],
        recent_run_rates: [4.2, 3.1, 1.5, 2.8, 3.0, 2.2],
        batting_first: true,
      },
    },
    {
      label: "😰 Chase Choke (145/6 chasing 285, over 35)",
      input: {
        match_format: "ODI",
        overs: 35,
        runs: 145,
        wickets: 6,
        total_overs: 50,
        recent_wickets: [
          { over: 30.4, runs_at_wicket: 120 },
          { over: 32.1, runs_at_wicket: 128 },
          { over: 34.3, runs_at_wicket: 138 },
        ],
        recent_run_rates: [5, 4, 3, 2, 3, 2],
        batting_first: false,
        target: 285,
      },
    },
    {
      label: "🏏 T20 Panic (78/5 chasing 186, over 12)",
      input: {
        match_format: "T20I",
        overs: 12,
        runs: 78,
        wickets: 5,
        total_overs: 20,
        recent_wickets: [
          { over: 9.3, runs_at_wicket: 58 },
          { over: 10.5, runs_at_wicket: 65 },
          { over: 11.4, runs_at_wicket: 72 },
        ],
        recent_run_rates: [8, 6, 4, 5, 3, 4],
        batting_first: false,
        target: 186,
      },
    },
  ];

  const patternList = patterns?.patterns || [];

  return (
    <div className="max-w-6xl space-y-8">
      {/* Simulation Panel */}
      <section>
        <h2 className="text-base font-bold mb-4 flex items-center gap-2">
          <Zap className="h-5 w-5 text-pak-green" />
          Collapse Simulator — Pick a Scenario
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {presetScenarios.map((s, i) => (
            <button
              key={i}
              onClick={() => runSimulation(s.input)}
              disabled={loading}
              className="rounded-xl bg-bg-card border border-border p-4 text-left hover:bg-bg-card-hover transition-all group"
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-text-primary">{s.label}</span>
                <Play className="h-4 w-4 text-text-muted group-hover:text-accent-green transition-colors" />
              </div>
              <p className="text-xs text-text-muted mt-1">
                {s.input.runs}/{s.input.wickets} in {s.input.overs} overs
                {s.input.target ? ` (chasing ${s.input.target})` : " (batting first)"}
              </p>
            </button>
          ))}
        </div>
      </section>

      {/* Simulation Result */}
      {simResult && (
        <section className="space-y-4">
          <h2 className="text-base font-bold flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-pak-green" />
            Collapse Analysis
          </h2>

          {/* Alert Level + Panic */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="rounded-xl bg-bg-card border border-border p-6 text-center">
              <span
                className={`inline-block px-4 py-2 rounded-full text-sm font-bold ${
                  alertBadgeStyles[simResult.alert_level] || "bg-bg-secondary text-text-primary"
                }`}
              >
                {simResult.alert_level}
              </span>
              <p className="text-xs text-text-muted mt-2">Alert Level</p>
            </div>
            <div className="rounded-xl bg-bg-card border border-border p-6 text-center">
              <div
                className={`text-4xl font-bold font-mono ${
                  simResult.panic_level >= 70
                    ? "text-accent-red"
                    : simResult.panic_level >= 40
                    ? "text-accent-orange"
                    : "text-accent-yellow"
                }`}
              >
                {simResult.panic_level}
              </div>
              <p className="text-xs text-text-muted mt-1">Panic Level / 100</p>
              <div className="w-full h-2 bg-bg-secondary rounded-full mt-3 overflow-hidden">
                <div
                  className={`h-full rounded-full ${
                    simResult.panic_level >= 70
                      ? "bg-accent-red"
                      : simResult.panic_level >= 40
                      ? "bg-accent-orange"
                      : "bg-accent-yellow"
                  }`}
                  style={{ width: `${simResult.panic_level}%` }}
                />
              </div>
            </div>
          </div>

          {/* Alerts */}
          {simResult.alerts?.length > 0 && (
            <div className="space-y-2">
              {simResult.alerts.map((a: any, i: number) => (
                <div
                  key={i}
                  className={`rounded-lg border p-3 text-sm ${
                    a.severity === "critical"
                      ? "bg-accent-red/20 border-accent-red/30 text-accent-red"
                      : "bg-accent-orange/20 border-accent-orange/30 text-accent-orange"
                  }`}
                >
                  {a.message}
                </div>
              ))}
            </div>
          )}

          {/* Matched Patterns */}
          {simResult.matched_patterns?.length > 0 && (
            <div className="rounded-xl bg-bg-card border border-border p-4">
              <h3 className="text-sm font-bold mb-2">Matched Collapse Patterns</h3>
              <div className="flex flex-wrap gap-2">
                {simResult.matched_patterns.map((p: string, i: number) => (
                  <span key={i} className="text-xs bg-accent-red/20 text-accent-red px-3 py-1 rounded-full">
                    {p}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Projection */}
          {simResult.projection && (
            <div className="rounded-xl bg-bg-card border border-border p-4">
              <h3 className="text-sm font-bold mb-3 flex items-center gap-2">
                <Skull className="h-4 w-4 text-accent-red" />
                Score Projection
              </h3>
              <div className="grid grid-cols-3 gap-4 mb-3">
                <div className="text-center">
                  <div className="text-xs text-text-muted">Worst Case</div>
                  <div className="text-xl font-bold font-mono text-accent-red">
                    {simResult.projection.worst_case}
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-xs text-text-muted">Most Likely</div>
                  <div className="text-xl font-bold font-mono text-accent-orange">
                    {simResult.projection.most_likely}
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-xs text-text-muted">Best Case</div>
                  <div className="text-xl font-bold font-mono text-accent-green">
                    {simResult.projection.best_case}
                  </div>
                </div>
              </div>
              <p className="text-sm text-text-secondary italic">
                {simResult.projection.message}
              </p>
            </div>
          )}
        </section>
      )}

      {/* Known Collapse Patterns */}
      <section>
        <h2 className="text-base font-bold mb-4 flex items-center gap-2">
          <BookOpen className="h-5 w-5 text-pak-green" />
          Know Your Collapses — Pakistan&apos;s Greatest Hits
        </h2>
        <div className="space-y-3">
          {patternList.map((p: any, i: number) => (
            <div key={i} className="rounded-xl bg-bg-card border border-border p-4">
              <h3 className="text-sm font-bold text-text-primary mb-1">{p.name}</h3>
              <p className="text-sm text-text-secondary mb-3">{p.description}</p>
              <div className="flex flex-wrap gap-2 mb-3">
                {p.trigger_conditions?.map((t: string, j: number) => (
                  <span key={j} className="text-xs bg-bg-secondary text-text-muted px-2 py-1 rounded-full">
                    {t}
                  </span>
                ))}
              </div>
              <div className="flex flex-wrap items-center gap-4 text-xs">
                <span className="text-accent-orange">{p.frequency}</span>
                <span className="text-text-muted">Last: {p.last_occurrence}</span>
              </div>
              {p.famous_examples && (
                <div className="mt-2 space-y-1">
                  {p.famous_examples.map((ex: string, k: number) => (
                    <p key={k} className="text-xs text-text-muted">
                      • {ex}
                    </p>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
