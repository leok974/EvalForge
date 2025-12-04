import React, { useState } from "react";

interface EvalResult {
    success: boolean;
    score: number;
    rubric?: Record<string, any>;
    integrity_before?: number;
    integrity_after?: number;
    integrity_delta?: number;
    boss_hp_before?: number;
    boss_hp_after?: number;
    boss_hp_delta?: number;
}

interface IntentOracleEvalButtonProps {
    endpoint?: string;
}

export const IntentOracleEvalButton: React.FC<IntentOracleEvalButtonProps> = ({
    endpoint = "/api/agents/intent-oracle/eval",
}) => {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<EvalResult | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleClick = async () => {
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            // In a real app, you might want to pass the candidate path or other args.
            // For now, the backend endpoint handles defaults or we could pass a payload.
            const res = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({}),
            });

            if (!res.ok) {
                const text = await res.text();
                throw new Error(`Eval failed: ${res.status} ${text}`);
            }

            const data = await res.json();
            setResult(data);
        } catch (err: any) {
            setError(err.message || String(err));
        } finally {
            setLoading(false);
        }
    };

    const statusColor = result?.success ? "text-emerald-400" : "text-rose-400";

    return (
        <div className="flex flex-col gap-2">
            <div className="flex items-center justify-between">
                <div className="flex flex-col">
                    <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                        Intent Oracle
                    </span>
                    <span className="text-[10px] text-slate-500">
                        Validate planner against boss logic
                    </span>
                </div>
                <button
                    onClick={handleClick}
                    disabled={loading}
                    className={`
            group relative overflow-hidden rounded-md border border-fuchsia-500/40 bg-fuchsia-900/20 px-3 py-1.5
            transition-all hover:border-fuchsia-400 hover:bg-fuchsia-900/40 hover:shadow-[0_0_15px_rgba(217,70,239,0.3)]
            disabled:cursor-not-allowed disabled:opacity-50
          `}
                >
                    {loading ? (
                        <span className="flex items-center gap-2 text-[11px] font-medium text-fuchsia-200">
                            <span className="h-2 w-2 animate-spin rounded-full border-2 border-current border-t-transparent" />
                            Running...
                        </span>
                    ) : (
                        <span className="text-[11px] font-medium text-fuchsia-200 group-hover:text-white">
                            Run Eval
                        </span>
                    )}
                </button>
            </div>

            <div className="mt-3 border-t border-fuchsia-500/25 pt-2.5 text-[11px] text-slate-300/90">
                {error && (
                    <div
                        className="rounded-lg border border-rose-500/60 bg-rose-900/20 px-2 py-1.5 text-[11px] text-rose-100"
                        data-testid="intent-oracle-eval-error"
                    >
                        Error: {error}
                    </div>
                )}

                {!error && result && (
                    <div className="flex flex-col gap-2" data-testid="intent-oracle-eval-result">
                        <div className="flex flex-wrap items-center justify-between gap-2">
                            <div className={statusColor}>
                                {result.success ? "Boss PASSED" : "Boss FAILED"}
                                {typeof result.score === "number" && (
                                    <>
                                        {" "}
                                        • Score:{" "}
                                        <span className="font-semibold">
                                            {(result.score * 100).toFixed(1)}%
                                        </span>
                                    </>
                                )}
                            </div>
                            {result.rubric && (
                                <button
                                    type="button"
                                    className="rounded-full border border-slate-600/70 bg-slate-900/70 px-2.5 py-1 text-[10px] text-slate-200 hover:border-slate-400/80"
                                    onClick={() => {
                                        // Simple dev-friendly view: log rubric to console
                                        // eslint-disable-next-line no-console
                                        console.log("Intent Oracle rubric", result.rubric);
                                        alert(
                                            "Rubric breakdown logged to console (open DevTools → Console)."
                                        );
                                    }}
                                    data-testid="intent-oracle-eval-rubric"
                                >
                                    View rubric breakdown
                                </button>
                            )}
                        </div>

                        {/* Combat Summary */}
                        {(result.integrity_delta !== undefined || result.boss_hp_delta !== undefined) && (
                            <div
                                className="mt-1 rounded-md border border-slate-700/50 bg-slate-950/50 px-2 py-1.5"
                                data-testid="intent-oracle-eval-meta"
                            >
                                <div className="flex items-center gap-4 text-[10px]">
                                    {result.integrity_before !== undefined && result.integrity_after !== undefined && (
                                        <div className="flex flex-col">
                                            <span className="text-slate-500 uppercase tracking-wider text-[9px]">Integrity</span>
                                            <span className="text-slate-300">
                                                {result.integrity_before} <span className="text-slate-600">→</span> {result.integrity_after}
                                                {result.integrity_delta !== 0 && (
                                                    <span className={result.integrity_delta! < 0 ? "ml-1 text-rose-400" : "ml-1 text-emerald-400"}>
                                                        ({result.integrity_delta! > 0 ? "+" : ""}{result.integrity_delta})
                                                    </span>
                                                )}
                                            </span>
                                        </div>
                                    )}
                                    {result.boss_hp_before !== undefined && result.boss_hp_after !== undefined && (
                                        <div className="flex flex-col">
                                            <span className="text-slate-500 uppercase tracking-wider text-[9px]">Boss HP</span>
                                            <span className="text-slate-300">
                                                {result.boss_hp_before} <span className="text-slate-600">→</span> {result.boss_hp_after}
                                                {result.boss_hp_delta !== 0 && (
                                                    <span className={result.boss_hp_delta! < 0 ? "ml-1 text-emerald-400" : "ml-1 text-rose-400"}>
                                                        ({result.boss_hp_delta! > 0 ? "+" : ""}{result.boss_hp_delta})
                                                    </span>
                                                )}
                                            </span>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {!error && !result && !loading && (
                    <p className="text-slate-400">
                        No eval run yet. Click{" "}
                        <span className="text-fuchsia-200">Run Eval</span> to benchmark the
                        planner against the Intent Oracle.
                    </p>
                )}
            </div>
        </div>
    );
};
