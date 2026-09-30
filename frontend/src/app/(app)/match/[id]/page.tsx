"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import { getMatchDetail, getCricbuzzScorecard } from "@/lib/api";
import Link from "next/link";
import {
  ArrowLeft,
  RefreshCw,
  AlertTriangle,
  TrendingDown,
  UserX,
  Activity,
  Target,
  BarChart3,
  MapPin,
  Calendar,
  Trophy,
  Coins,
} from "lucide-react";

/* eslint-disable @typescript-eslint/no-explicit-any */

const alertColors: Record<string, { bg: string; text: string }> = {
  MELTDOWN: { bg: "bg-alert-meltdown/20 border-alert-meltdown/30", text: "text-alert-meltdown" },
  COLLAPSE_INCOMING: { bg: "bg-alert-collapse/20 border-alert-collapse/30", text: "text-alert-collapse" },
  CHOKING: { bg: "bg-alert-choking/20 border-alert-choking/30", text: "text-alert-choking" },
  NERVOUS: { bg: "bg-alert-nervous/20 border-alert-nervous/30", text: "text-alert-nervous" },
  STABLE: { bg: "bg-alert-stable/20 border-alert-stable/30", text: "text-alert-stable" },
};

const fraudColors: Record<string, string> = {
  "certified-fraud": "text-fraud-certified",
  suspect: "text-fraud-suspect",
  underperformer: "text-fraud-under",
  inconsistent: "text-fraud-inconsistent",
  redeemable: "text-fraud-redeemable",
};

export default function MatchDetailPage() {
  const params = useParams();
  const matchId = params.id as string;
  const [data, setData] = useState<any>(null);
  const [cbScorecard, setCbScorecard] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const isCricbuzz = matchId?.startsWith("cb_");
  const realCbId = isCricbuzz ? matchId.replace("cb_", "") : null;

  const fetchData = useCallback(async () => {
    if (!matchId) return;
    setLoading(true);
    setError("");
    try {
      if (isCricbuzz && realCbId) {
        // Cricbuzz match - fetch scorecard directly
        const sc = await getCricbuzzScorecard(realCbId);
        setCbScorecard(sc);
      } else {
        // CricAPI match - fetch detail + try Cricbuzz scorecard as supplement
        const [detail] = await Promise.all([
          getMatchDetail(matchId).catch(() => null),
        ]);
        if (detail && !(detail as any).error) {
          setData(detail);
        } else {
          setError((detail as any)?.error || "Could not load match");
        }
      }
    } catch {
      setError("Could not load match data.");
    } finally {
      setLoading(false);
    }
  }, [matchId, isCricbuzz, realCbId]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (loading) return <LoadingState />;

  // Choose which data to render
  const hasCb = cbScorecard && !cbScorecard.error && cbScorecard.innings?.length > 0;
  const hasApi = data && !data.error;

  if (!hasCb && !hasApi && error) {
    return <ErrorState error={error} />;
  }

  const matchName = hasCb ? cbScorecard.name : data?.name || "";
  const statusText = hasCb ? cbScorecard.status_text : data?.status_text || "";
  const lossAnalysis = data?.loss_analysis || null;
  const fraudAlerts = data?.fraud_alerts || [];

  return (
    <div className="max-w-6xl space-y-6">
      {/* Back + Refresh */}
      <div className="flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 text-sm text-pak-green hover:underline">
          <ArrowLeft className="h-4 w-4" /> Back to matches
        </Link>
        <button
          onClick={fetchData}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs text-text-muted hover:text-pak-green bg-bg-card border border-border hover:border-pak-green/20 transition-all"
        >
          <RefreshCw className="h-3.5 w-3.5" /> Refresh
        </button>
      </div>

      {/* Match Header */}
      <div className="rounded-xl bg-bg-card border border-border p-5">
        <h2 className="text-lg font-bold text-text-primary">{matchName}</h2>
        <div className="flex flex-wrap items-center gap-3 mt-2 text-xs text-text-muted">
          {data?.match_type && (
            <span className="bg-pak-green-dim text-pak-green px-2.5 py-0.5 rounded-full font-medium">
              {data.match_type}
            </span>
          )}
          {data?.venue && (
            <span className="flex items-center gap-1"><MapPin className="h-3 w-3" />{data.venue}</span>
          )}
          {data?.date && (
            <span className="flex items-center gap-1"><Calendar className="h-3 w-3" />{data.date}</span>
          )}
          {hasCb && (
            <span className="bg-accent-blue/20 text-accent-blue px-2 py-0.5 rounded-full text-[10px]">
              Full Scorecard via Cricbuzz
            </span>
          )}
        </div>
        {data?.toss_winner && (
          <p className="mt-2 flex items-center gap-2 text-xs text-text-muted">
            <Coins className="h-3.5 w-3.5 text-accent-yellow" />
            <strong className="text-text-secondary">{data.toss_winner}</strong> won toss, chose to <strong className="text-text-secondary">{data.toss_choice}</strong>
          </p>
        )}
        {statusText && (
          <p className="mt-2 text-sm font-medium text-pak-green flex items-center gap-2">
            <Trophy className="h-4 w-4 text-accent-yellow" />
            {statusText}
          </p>
        )}
      </div>

      {/* Main layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Scorecard - 2 cols */}
        <div className="lg:col-span-2 space-y-4">
          {/* CricAPI innings summary (always show if available) */}
          {hasApi && data.scores?.length > 0 && (
            <div className="rounded-xl bg-bg-card border border-border overflow-hidden">
              <div className="bg-pak-dark-dim border-b border-border px-4 py-3">
                <h3 className="text-sm font-bold text-text-primary">Innings Summary</h3>
              </div>
              <div className="divide-y divide-border">
                {data.scores.map((s: any, i: number) => {
                  const isPak = (s.inning || "").toLowerCase().includes("pakistan");
                  return (
                    <div key={i} className="px-4 py-3 flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className={`h-2 w-2 rounded-full ${isPak ? "bg-pak-green" : "bg-text-muted"}`} />
                        <span className={`text-sm font-medium ${isPak ? "text-pak-green" : "text-text-primary"}`}>
                          {s.inning}
                        </span>
                      </div>
                      <span className="text-sm font-mono font-bold text-text-primary">
                        {s.runs}/{s.wickets} <span className="text-text-muted font-normal">({s.overs} ov)</span>
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Cricbuzz full batting/bowling tables */}
          {hasCb && cbScorecard.innings.map((inn: any, i: number) => (
            <div key={i} className="space-y-4">
              {/* Batting Table */}
              {inn.batting?.length > 0 && (
                <div className="rounded-xl bg-bg-card border border-border overflow-hidden">
                  <div className="bg-pak-dark-dim border-b border-border px-4 py-3">
                    <h3 className="text-sm font-bold text-text-primary">Batting</h3>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs">
                      <thead>
                        <tr className="border-b border-border text-text-muted bg-bg-secondary/50">
                          <th className="text-left px-4 py-2.5 font-medium">Batter</th>
                          <th className="text-left px-2 py-2.5 font-medium hidden sm:table-cell">Dismissal</th>
                          <th className="text-right px-2 py-2.5 font-medium">R</th>
                          <th className="text-right px-2 py-2.5 font-medium">B</th>
                          <th className="text-right px-2 py-2.5 font-medium">4s</th>
                          <th className="text-right px-2 py-2.5 font-medium">6s</th>
                          <th className="text-right px-4 py-2.5 font-medium">SR</th>
                        </tr>
                      </thead>
                      <tbody>
                        {inn.batting.map((b: any, j: number) => (
                          <tr key={j} className="border-b border-border/40 hover:bg-bg-card-hover transition-colors">
                            <td className="px-4 py-2.5 font-medium text-text-primary">{b.name}</td>
                            <td className="px-2 py-2.5 text-text-muted truncate max-w-[180px] hidden sm:table-cell">{b.dismissal}</td>
                            <td className="px-2 py-2.5 text-right font-mono font-bold text-text-primary">{b.runs}</td>
                            <td className="px-2 py-2.5 text-right font-mono text-text-muted">{b.balls}</td>
                            <td className="px-2 py-2.5 text-right font-mono text-text-muted">{b.fours}</td>
                            <td className="px-2 py-2.5 text-right font-mono text-text-muted">{b.sixes}</td>
                            <td className="px-4 py-2.5 text-right font-mono text-text-muted">{b.strike_rate}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Bowling Table */}
              {inn.bowling?.length > 0 && (
                <div className="rounded-xl bg-bg-card border border-border overflow-hidden">
                  <div className="bg-pak-dark-dim border-b border-border px-4 py-3">
                    <h3 className="text-sm font-bold text-text-primary">Bowling</h3>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs">
                      <thead>
                        <tr className="border-b border-border text-text-muted bg-bg-secondary/50">
                          <th className="text-left px-4 py-2.5 font-medium">Bowler</th>
                          <th className="text-right px-2 py-2.5 font-medium">O</th>
                          <th className="text-right px-2 py-2.5 font-medium">M</th>
                          <th className="text-right px-2 py-2.5 font-medium">R</th>
                          <th className="text-right px-2 py-2.5 font-medium">W</th>
                          <th className="text-right px-4 py-2.5 font-medium">Econ</th>
                        </tr>
                      </thead>
                      <tbody>
                        {inn.bowling.map((bw: any, j: number) => (
                          <tr key={j} className="border-b border-border/40 hover:bg-bg-card-hover transition-colors">
                            <td className="px-4 py-2.5 font-medium text-text-primary">{bw.name}</td>
                            <td className="px-2 py-2.5 text-right font-mono text-text-muted">{bw.overs}</td>
                            <td className="px-2 py-2.5 text-right font-mono text-text-muted">{bw.maidens}</td>
                            <td className="px-2 py-2.5 text-right font-mono text-text-muted">{bw.runs}</td>
                            <td className="px-2 py-2.5 text-right font-mono font-bold text-text-primary">{bw.wickets}</td>
                            <td className="px-4 py-2.5 text-right font-mono text-text-muted">{bw.economy}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          ))}

          {/* No scorecard available */}
          {!hasCb && (!hasApi || !data.scores?.length) && (
            <div className="rounded-xl bg-bg-card border border-border p-8 text-center">
              <BarChart3 className="h-8 w-8 text-text-muted mx-auto mb-2" />
              <p className="text-sm text-text-muted">No scorecard data available for this match</p>
            </div>
          )}
        </div>

        {/* Sidebar - 1 col */}
        <div className="space-y-4">
          {lossAnalysis && <LossPanel analysis={lossAnalysis} />}
          {fraudAlerts.length > 0 && <FraudPanel alerts={fraudAlerts} />}
        </div>
      </div>
    </div>
  );
}

function LossPanel({ analysis }: { analysis: any }) {
  const alert = alertColors[analysis.alert_level] || alertColors.STABLE;
  return (
    <div className="rounded-xl bg-bg-card border border-border overflow-hidden">
      <div className="bg-pak-dark-dim border-b border-border px-4 py-3">
        <h3 className="text-sm font-bold text-text-primary flex items-center gap-2">
          <TrendingDown className="h-4 w-4 text-accent-red" />
          Pakistan Loss Probability
        </h3>
      </div>
      <div className="p-4 space-y-4">
        <div className={`rounded-lg border px-3 py-2 text-center ${alert.bg}`}>
          <span className={`text-xs font-bold ${alert.text}`}>{analysis.alert_level}</span>
        </div>
        <div className="text-center">
          <div className={`text-4xl font-bold font-mono ${
            analysis.loss_probability >= 70 ? "text-accent-red" :
            analysis.loss_probability >= 50 ? "text-accent-orange" :
            analysis.loss_probability >= 30 ? "text-accent-yellow" : "text-pak-green"
          }`}>{analysis.loss_probability}%</div>
          <div className="text-xs text-text-muted mt-1">Chance of Losing</div>
        </div>
        <div className="w-full h-2.5 bg-bg-secondary rounded-full overflow-hidden">
          <div className={`h-full rounded-full ${
            analysis.loss_probability >= 70 ? "bg-accent-red" :
            analysis.loss_probability >= 50 ? "bg-accent-orange" :
            analysis.loss_probability >= 30 ? "bg-accent-yellow" : "bg-pak-green"
          }`} style={{ width: `${analysis.loss_probability}%` }} />
        </div>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <MiniStat label="Win %" value={`${analysis.win_probability}%`} icon={<Target className="h-3 w-3 text-pak-green" />} />
          <MiniStat label="Collapse Risk" value={`${analysis.collapse_risk}%`} icon={<AlertTriangle className="h-3 w-3 text-accent-orange" />} />
          <MiniStat label="Run Rate" value={analysis.current_run_rate} icon={<Activity className="h-3 w-3 text-accent-blue" />} />
          <MiniStat label="Projected" value={analysis.projected_score} icon={<BarChart3 className="h-3 w-3 text-accent-purple" />} />
        </div>
        {analysis.key_factors?.length > 0 && (
          <div className="space-y-1 pt-2 border-t border-border">
            {analysis.key_factors.map((f: string, i: number) => (
              <p key={i} className="text-xs text-text-secondary">{f}</p>
            ))}
          </div>
        )}
        {analysis.historical_comparison && (
          <p className="text-xs text-text-muted italic border-t border-border pt-3">📊 {analysis.historical_comparison}</p>
        )}
      </div>
    </div>
  );
}

function FraudPanel({ alerts }: { alerts: any[] }) {
  return (
    <div className="rounded-xl bg-bg-card border border-border overflow-hidden">
      <div className="bg-pak-dark-dim border-b border-border px-4 py-3">
        <h3 className="text-sm font-bold text-text-primary flex items-center gap-2">
          <UserX className="h-4 w-4 text-accent-orange" />
          Player Fraud Watch
        </h3>
      </div>
      <div className="p-4 space-y-3 max-h-[600px] overflow-y-auto">
        {alerts.map((a: any, i: number) => (
          <div key={i} className="rounded-lg bg-bg-secondary border border-border p-3">
            <div className="flex items-center justify-between mb-1.5">
              <div>
                <span className="text-xs font-bold text-text-primary">{a.player_name}</span>
                <span className="text-[10px] text-text-muted ml-2">{a.role}</span>
              </div>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${fraudColors[a.fraud_rating] || ""} bg-bg-card`}>
                {a.rating_display?.emoji} {a.rating_display?.label}
              </span>
            </div>
            <div className="text-[10px] text-text-muted">Score: {a.fraud_score}/100</div>
            {a.red_flags?.slice(0, 1).map((rf: any, j: number) => (
              <p key={j} className="text-[10px] text-accent-orange mt-1">⚠ {rf.flag}</p>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

function MiniStat({ label, value, icon }: { label: string; value: any; icon: React.ReactNode }) {
  return (
    <div className="rounded-lg bg-bg-secondary p-2">
      <div className="flex items-center gap-1 mb-0.5">{icon}<span className="text-text-muted">{label}</span></div>
      <div className="font-mono font-bold text-text-primary">{value}</div>
    </div>
  );
}

function LoadingState() {
  return (
    <div className="max-w-6xl space-y-4">
      <div className="h-8 w-32 bg-bg-card rounded animate-pulse" />
      <div className="h-48 bg-bg-card rounded-xl animate-pulse" />
      <div className="h-64 bg-bg-card rounded-xl animate-pulse" />
    </div>
  );
}

function ErrorState({ error }: { error: string }) {
  return (
    <div className="max-w-6xl">
      <Link href="/" className="flex items-center gap-2 text-sm text-pak-green mb-4 hover:underline">
        <ArrowLeft className="h-4 w-4" /> Back to matches
      </Link>
      <div className="rounded-xl bg-bg-card border border-border p-12 text-center">
        <AlertTriangle className="h-10 w-10 text-accent-orange mx-auto mb-3" />
        <p className="text-text-secondary font-medium">{error}</p>
      </div>
    </div>
  );
}
