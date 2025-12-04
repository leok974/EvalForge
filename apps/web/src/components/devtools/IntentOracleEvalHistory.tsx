import React, { useEffect, useState } from "react";

interface EvalRun {
    id: string;
    timestamp: string;
    success: boolean;
    score?: number | null;
    candidate_path?: string | null;
    source?: string | null;
}

interface HistoryResponse {
    runs: EvalRun[];
}

interface IntentOracleEvalHistoryProps {
    endpoint?: string;
    limit?: number;
}

export const IntentOracleEvalHistory: React.FC<IntentOracleEvalHistoryProps> = ({
    endpoint = "/api/agents/intent-oracle/eval/history",
    limit = 5,
}) => {
    const [runs, setRuns] = useState<EvalRun[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let cancelled = false;
        async function load() {
            setLoading(true);
            setError(null);
            try {
                const res = await fetch(`${endpoint}?limit=${limit}`);
                if (!res.ok) {
                    const text = await res.text();
                    throw new Error(
                        `Failed to load history (${res.status}): ${text.slice(0, 200)}`
                    );
                }
                const data: HistoryResponse = await res.json();
                if (!cancelled) {
                    setRuns(data.runs ?? []);
                }
            } catch (err: any) {
                if (!cancelled) {
                    console.error("Failed to load Intent Oracle eval history", err);
                    setError(err?.message ?? "Unknown error");
                }
            } finally {
                if (!cancelled) setLoading(false);
            }
        }
        load();
        return () => {
            cancelled = true;
        };
    }, [endpoint, limit]);

    return (
        <div
            className={`
        rounded-2xl border border-cyan-500/45 bg-slate-950/80
        px-3 py-3.5 sm:px-4 sm:py-4 shadow-[0_0_30px_rgba(34,211,238,0.35)]
      `}
            data-testid="intent-oracle-eval-history"
        >
            <div className="flex items-center justify-between gap-2">
                <div>
                    <div className="inline-flex items-center gap-1.5 rounded-full border border-cyan-400/70 bg-cyan-900/30 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.16em] text-cyan-100">
                        <span className="h-1.5 w-1.5 rounded-full bg-cyan-300" />
                        Planner Eval History
                    </div>
                    <p className="mt-1 text-xs text-slate-300/80">
                        Last {limit} runs against the{" "}
                        <span className="text-cyan-200">Intent Oracle</span> boss.
                    </p>
                </div>
            </div>

            <div className="mt-3 border-t border-cyan-500/25 pt-2.5 text-[11px]">
                {loading && (
                    <p className="text-slate-400">Loading eval history…</p>
                )}

                {error && !loading && (
                    <div className="rounded-lg border border-rose-500/60 bg-rose-900/20 px-2 py-1.5 text-[11px] text-rose-100">
                        Error loading history: {error}
                    </div>
                )}

                {!loading && !error && runs.length === 0 && (
                    <p className="text-slate-400">
                        No eval runs yet. Trigger a run via{" "}
                        <span className="text-cyan-200">Run Eval</span> to populate this
                        list.
                    </p>
                )}

                {!loading && !error && runs.length > 0 && (
                    <div className="mt-1 space-y-1.5 max-h-56 overflow-y-auto pr-1">
                        {runs.map((run) => {
                            const scorePct =
                                typeof run.score === "number"
                                    ? (run.score * 100).toFixed(1)
                                    : null;
                            const ts = new Date(run.timestamp);
                            const tsLabel = ts.toLocaleString(undefined, {
                                month: "short",
                                day: "2-digit",
                                hour: "2-digit",
                                minute: "2-digit",
                            });
                            const statusColor = run.success
                                ? "text-emerald-300"
                                : "text-rose-300";

                            return (
                                <div
                                    key={run.id}
                                    className="flex items-center justify-between gap-2 rounded-lg border border-slate-700/60 bg-slate-950/80 px-2 py-1.5"
                                >
                                    <div className="flex min-w-0 flex-col">
                                        <div className="flex items-center gap-2">
                                            <span className={`text-[11px] font-semibold ${statusColor}`}>
                                                {run.success ? "PASS" : "FAIL"}
                                            </span>
                                            {scorePct && (
                                                <span className="rounded-full bg-slate-900/80 px-1.5 py-[1px] text-[10px] text-slate-100 border border-slate-600/70">
                                                    {scorePct}%
                                                </span>
                                            )}
                                        </div>
                                        <div className="mt-[1px] flex flex-wrap items-center gap-1 text-[10px] text-slate-400">
                                            <span>{tsLabel}</span>
                                            {run.candidate_path && (
                                                <>
                                                    <span className="text-slate-600">•</span>
                                                    <span className="truncate max-w-[180px]">
                                                        {run.candidate_path}
                                                    </span>
                                                </>
                                            )}
                                            {run.source && (
                                                <>
                                                    <span className="text-slate-600">•</span>
                                                    <span className="text-slate-300/90">
                                                        {run.source}
                                                    </span>
                                                </>
                                            )}
                                        </div>
                                    </div>
                                    <button
                                        type="button"
                                        className="rounded-full border border-slate-600/70 bg-slate-900/70 px-2 py-0.5 text-[10px] text-slate-200 hover:border-slate-400/80"
                                        onClick={() => {
                                            // Log full raw run for deep debugging
                                            // eslint-disable-next-line no-console
                                            console.log("Intent Oracle eval run", run.id, run);
                                            alert(
                                                "Full run details logged to console (DevTools → Console)."
                                            );
                                        }}
                                    >
                                        Details
                                    </button>
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>
        </div>
    );
};
