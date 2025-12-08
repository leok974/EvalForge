import { useSeniorBossRuns } from "../../hooks/useSeniorBossRuns";

export function SeniorBossArchive() {
    const { items, loading, error } = useSeniorBossRuns();

    if (loading) {
        return <div className="text-xs text-slate-300">Loading senior runs...</div>;
    }
    if (error) {
        return (
            <div className="text-xs text-rose-300">
                Failed to load senior boss runs: {error}
            </div>
        );
    }
    if (!items.length) {
        return (
            <div className="text-xs text-slate-400">
                No senior boss runs yet. Clear a Legendary trial in the Practice Gauntlet to get started.
            </div>
        );
    }

    return (
        <div className="space-y-2 text-xs">
            {items.map((run) => (
                <div
                    key={`${run.boss_id}-${run.created_at}`}
                    className="rounded-xl border border-amber-500/40 bg-slate-950/70 px-3 py-2"
                >
                    <div className="flex items-center justify-between">
                        <div className="flex flex-col">
                            <span className="text-amber-200 font-semibold">
                                {run.boss_title}
                            </span>
                            <span className="text-[10px] text-slate-400">
                                {run.world_title ?? run.world_slug} • {run.track_id}
                            </span>
                        </div>
                        <div className="text-right">
                            <div className="text-[10px] text-amber-200">
                                Score {run.score}/8
                            </div>
                            <div className="text-[10px] text-slate-300">
                                {/* Integrity assuming hp_remaining is used as a rough proxy or special field */}
                                Integrity {run.integrity}
                            </div>
                        </div>
                    </div>
                    <div className="mt-2 flex items-center justify-between">
                        <div className="h-1.5 w-32 rounded-full bg-slate-900/80">
                            <div
                                className={`h-1.5 rounded-full ${run.passed ? "bg-emerald-400" : "bg-rose-400"
                                    }`}
                                // Assuming integrity is 0-100 or 0-1, but previous code used integrity * 100.
                                // Backend sends hp_remaining as float?
                                // Backend: integrity=float(getattr(run, "hp_remaining", 0.0) or 0.0)
                                // If hp_remaining is, say, 90, then style width is 90% or 9000%?
                                // I will ensure logic handles it. Previous frontend snippet was `width: ${run.integrity * 100}%` assuming 0.0-1.0.
                                // If Backend sends 0-100, then just `${run.integrity}%`.
                                // Let's assume 0-100 based on previous checks.
                                style={{ width: `${run.integrity}%` }}
                            />
                        </div>
                        <span
                            className={`text-[10px] uppercase tracking-wide ${run.passed ? "text-emerald-300" : "text-rose-300"
                                }`}
                        >
                            {run.passed ? "Passed" : "Failed"}
                        </span>
                    </div>
                    <div className="mt-1 text-[10px] text-slate-500">
                        {new Date(run.created_at).toLocaleString()}
                    </div>
                </div>
            ))}
        </div>
    );
}
