"use client";

import { useEffect, useState } from "react";
import { getFraudProfiles } from "@/lib/api";
import {
  UserX,
  AlertTriangle,
  TrendingDown,
  ChevronDown,
  ChevronUp,
  Shield,
  Target,
  BarChart3,
  Zap,
  Activity,
  MessageSquare,
} from "lucide-react";

/* eslint-disable @typescript-eslint/no-explicit-any */

const fraudBadgeStyles: Record<string, { bg: string; text: string }> = {
  "certified-fraud": { bg: "bg-fraud-certified/20", text: "text-fraud-certified" },
  suspect: { bg: "bg-fraud-suspect/20", text: "text-fraud-suspect" },
  underperformer: { bg: "bg-fraud-under/20", text: "text-fraud-under" },
  inconsistent: { bg: "bg-fraud-inconsistent/20", text: "text-fraud-inconsistent" },
  redeemable: { bg: "bg-fraud-redeemable/20", text: "text-fraud-redeemable" },
};

export default function FraudPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [filterRating, setFilterRating] = useState<string>("");

  useEffect(() => {
    getFraudProfiles()
      .then(setData)
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

  if (!data) {
    return (
      <div className="rounded-xl bg-bg-card border border-border p-12 text-center max-w-6xl">
        <AlertTriangle className="h-8 w-8 text-accent-orange mx-auto mb-3" />
        <p className="text-sm text-text-muted">
          Backend not running. Start it with: cd backend && uvicorn app.main:app --reload
        </p>
      </div>
    );
  }

  const players = data.players || [];
  const filteredPlayers = filterRating
    ? players.filter((p: any) => p.computed_fraud_rating === filterRating)
    : players;

  return (
    <div className="max-w-6xl space-y-6">
      {/* Fraud Formula Explanation */}
      <div className="rounded-xl bg-pak-dark-dim border border-pak-green/20 p-5">
        <h3 className="text-sm font-bold text-pak-green mb-3">📊 How We Calculate the Fraud Score (T20I Only)</h3>
        <p className="text-xs text-text-secondary mb-3">
          Each player gets a score from 0-100. Lower = bigger fraud. The score is computed from 4 components weighted by importance:
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <div className="bg-bg-card rounded-lg p-3 border border-border">
            <div className="font-bold text-text-primary mb-1">🏆 Match-Winning Ability - 30%</div>
            <p className="text-text-muted">Man of the Match awards vs Test-playing nations (not associates). Successful chase rate vs top teams. ICC knockout batting average. More MOMs vs real teams = higher score.</p>
          </div>
          <div className="bg-bg-card rounded-lg p-3 border border-border">
            <div className="font-bold text-text-primary mb-1">⚡ Strike Rate Analysis - 25%</div>
            <p className="text-text-muted">Overall T20I SR (under 130 = criminal). SR vs Test nations specifically. Gap between SR vs associates and SR vs Test nations - a big gap means stat-padding. Fakhar&apos;s 132 SR &gt; Babar&apos;s 128 SR.</p>
          </div>
          <div className="bg-bg-card rounded-lg p-3 border border-border">
            <div className="font-bold text-text-primary mb-1">🏏 ICC Tournament Performance - 25%</div>
            <p className="text-text-muted">T20 World Cup average and strike rate. Powerplay SR in World Cups (Babar: 86, Rizwan: 98 - fraud territory). ICC knockout average (both under 14 - certified fraud).</p>
          </div>
          <div className="bg-bg-card rounded-lg p-3 border border-border">
            <div className="font-bold text-text-primary mb-1">📈 Consistency &amp; Trend - 20%</div>
            <p className="text-text-muted">Is performance improving or declining? Big match failure rate. Players dropped from the squad get penalized. SR trend matters more than average trend in T20s.</p>
          </div>
        </div>
        <div className="mt-3 text-[10px] text-text-muted">
          <span className="text-fraud-certified font-bold">0-25: CERTIFIED FRAUD</span> · <span className="text-fraud-suspect font-bold">25-40: SUSPECT</span> · <span className="text-fraud-under font-bold">40-55: UNDERPERFORMER</span> · <span className="text-fraud-inconsistent font-bold">55-70: INCONSISTENT</span> · <span className="text-fraud-redeemable font-bold">70+: REDEEMABLE</span>
        </div>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {[
          { label: "Certified Frauds", count: data.rating_summary?.certified_frauds || 0, rating: "certified-fraud" },
          { label: "Suspects", count: data.rating_summary?.suspects || 0, rating: "suspect" },
          { label: "Underperformers", count: data.rating_summary?.underperformers || 0, rating: "underperformer" },
          { label: "Inconsistent", count: data.rating_summary?.inconsistent || 0, rating: "inconsistent" },
          { label: "Redeemable", count: data.rating_summary?.redeemable || 0, rating: "redeemable" },
        ].map((item) => (
          <button
            key={item.rating}
            onClick={() => setFilterRating(filterRating === item.rating ? "" : item.rating)}
            className={`rounded-xl border p-3 text-center transition-all ${
              filterRating === item.rating
                ? `${fraudBadgeStyles[item.rating].bg} border-current`
                : "bg-bg-card border-border hover:bg-bg-card-hover"
            }`}
          >
            <div className={`text-2xl font-bold font-mono ${fraudBadgeStyles[item.rating].text}`}>
              {item.count}
            </div>
            <div className="text-xs text-text-muted mt-1">{item.label}</div>
          </button>
        ))}
      </div>

      {/* Player Cards */}
      <div className="space-y-3">
        {filteredPlayers.map((player: any) => (
          <PlayerFraudCard
            key={player.id}
            player={player}
            expanded={expandedId === player.id}
            onToggle={() =>
              setExpandedId(expandedId === player.id ? null : player.id)
            }
          />
        ))}
      </div>
    </div>
  );
}

function PlayerFraudCard({
  player,
  expanded,
  onToggle,
}: {
  player: any;
  expanded: boolean;
  onToggle: () => void;
}) {
  const rating = player.computed_fraud_rating || player.fraud_rating;
  const ratingDisplay = player.rating_display || {};
  const badge = fraudBadgeStyles[rating] || fraudBadgeStyles["inconsistent"];

  return (
    <div className="rounded-xl bg-bg-card border border-border overflow-hidden">
      {/* Header */}
      <button
        onClick={onToggle}
        className="w-full p-4 flex items-center justify-between hover:bg-bg-card-hover transition-all"
      >
        <div className="flex items-center gap-4">
          <div
            className={`h-12 w-12 rounded-full ${badge.bg} flex items-center justify-center`}
          >
            <UserX className={`h-6 w-6 ${badge.text}`} />
          </div>
          <div className="text-left">
            <div className="flex items-center gap-2">
              <span className="font-bold text-text-primary">{player.name}</span>
              {player.real_name && (
                <span className="text-xs text-text-muted">({player.real_name})</span>
              )}
              <span className="text-xs text-text-muted">{player.role}</span>
            </div>
            <div className="flex items-center gap-2 mt-1">
              <span
                className={`text-xs font-bold px-2 py-0.5 rounded-full ${badge.bg} ${badge.text}`}
              >
                {ratingDisplay.emoji} {ratingDisplay.label || rating.toUpperCase()}
              </span>
              <span className="text-xs text-text-muted">
                Score: {player.computed_overall_score}/100
              </span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-right hidden md:block">
            <div
              className={`text-2xl font-bold font-mono ${
                player.computed_overall_score < 35
                  ? "text-accent-red"
                  : player.computed_overall_score < 55
                  ? "text-accent-orange"
                  : "text-accent-yellow"
              }`}
            >
              {player.computed_overall_score}
            </div>
            <div className="text-xs text-text-muted">Fraud Score</div>
          </div>
          {expanded ? (
            <ChevronUp className="h-5 w-5 text-text-muted" />
          ) : (
            <ChevronDown className="h-5 w-5 text-text-muted" />
          )}
        </div>
      </button>

      {/* Expanded Content */}
      {expanded && (
        <div className="border-t border-border p-4 space-y-4">
          {/* Component Scores */}
          <div>
            <h4 className="text-xs font-bold text-text-muted uppercase mb-3">
              Fraud Detection Components
            </h4>
            <div className="space-y-2">
              {player.fraud_components &&
                Object.entries(player.fraud_components).map(
                  ([key, comp]: [string, any]) => (
                    <div key={key}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-text-secondary">
                          {comp.description}
                        </span>
                        <span className="text-xs font-mono font-bold text-text-primary">
                          {comp.score}/100
                        </span>
                      </div>
                      <div className="w-full h-2 bg-bg-secondary rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${
                            comp.score < 35
                              ? "bg-accent-red"
                              : comp.score < 55
                              ? "bg-accent-orange"
                              : comp.score < 70
                              ? "bg-accent-yellow"
                              : "bg-accent-green"
                          }`}
                          style={{ width: `${comp.score}%` }}
                        />
                      </div>
                    </div>
                  )
                )}
            </div>
          </div>

          {/* Red Flags */}
          {player.red_flags?.length > 0 && (
            <div>
              <h4 className="text-xs font-bold text-text-muted uppercase mb-2 flex items-center gap-1">
                <AlertTriangle className="h-3 w-3 text-accent-red" />
                Red Flags
              </h4>
              <div className="space-y-2">
                {player.red_flags.map((flag: any, i: number) => (
                  <div
                    key={i}
                    className={`rounded-lg p-3 text-sm ${
                      flag.severity === "critical"
                        ? "bg-accent-red/20 border border-accent-red/20"
                        : "bg-accent-orange/20 border border-accent-orange/20"
                    }`}
                  >
                    <div className="font-medium text-text-primary text-xs mb-1">
                      {flag.flag}
                    </div>
                    <div className="text-xs text-text-secondary">{flag.evidence}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Performance Trend */}
          {player.performance_trend?.length > 0 && (
            <div>
              <h4 className="text-xs font-bold text-text-muted uppercase mb-2 flex items-center gap-1">
                <TrendingDown className="h-3 w-3 text-accent-orange" />
                Performance Trend (Strike Rate)
              </h4>
              <div className="flex gap-1 items-end h-24">
                {player.performance_trend
                  .filter((t: any) => t.matches > 0)
                  .map((t: any, i: number) => {
                  const val = t.strike_rate || t.average || 0;
                  const allVals = player.performance_trend
                    .filter((x: any) => x.matches > 0)
                    .map((x: any) => x.strike_rate || x.average || 0);
                  const maxVal = Math.max(...allVals, 1);
                  const height = Math.max((val / maxVal) * 100, 4);
                  return (
                    <div key={i} className="flex-1 flex flex-col items-center gap-1" title={`${t.period}: SR ${t.strike_rate}, Avg ${t.average}, ${t.matches} matches`}>
                      <span className="text-[8px] text-text-muted font-mono">{Math.round(val)}</span>
                      <div
                        className={`w-full rounded-t min-h-[3px] ${
                          val < 115 ? "bg-accent-red" : val < 130 ? "bg-accent-orange" : val < 140 ? "bg-accent-yellow" : "bg-pak-green"
                        }`}
                        style={{ height: `${height}%` }}
                      />
                      <span className="text-[7px] text-text-muted whitespace-nowrap">
                        {t.period}
                      </span>
                    </div>
                  );
                })}
              </div>
              <p className="text-[9px] text-text-muted mt-1 italic">Bars show T20I strike rate per period. Red &lt; 115, Orange &lt; 130, Green 140+</p>
            </div>
          )}

          {/* Excuse Generator */}
          {player.excuse_generator?.length > 0 && (
            <div>
              <h4 className="text-xs font-bold text-text-muted uppercase mb-2 flex items-center gap-1">
                <MessageSquare className="h-3 w-3 text-accent-purple" />
                Fan Excuse Generator
              </h4>
              <div className="flex flex-wrap gap-2">
                {player.excuse_generator.map((e: string, i: number) => (
                  <span
                    key={i}
                    className="text-xs bg-bg-secondary text-text-muted px-2 py-1 rounded-full italic"
                  >
                    &ldquo;{e}&rdquo;
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Verdict */}
          <div className="rounded-lg bg-bg-secondary p-3">
            <h4 className="text-xs font-bold text-fraud-certified mb-1">VERDICT</h4>
            <p className="text-sm text-text-secondary">
              {player.verdict_summary}
            </p>
          </div>

          {/* Engine Analysis */}
          <div className="rounded-lg bg-bg-secondary p-3">
            <h4 className="text-xs font-bold text-accent-blue mb-1">
              ENGINE ANALYSIS
            </h4>
            <p className="text-sm text-text-secondary italic">
              {player.fraud_analysis}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
