import { useEffect, useState } from 'react';
import { Trophy, Skull } from 'lucide-react';

interface BossRun {
    boss_id: string;
    boss_name: string;
    difficulty: 'normal' | 'hard' | string;
    score: number;
    passed: boolean;
    integrity_delta: number;
    xp_awarded: number;
    created_at: string;
}

export function BossHistoryPanel() {
    const [runs, setRuns] = useState<BossRun[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let cancelled = false;
        (async () => {
            try {
                const res = await fetch('/api/boss/history?limit=5', { credentials: 'include' });
                if (!res.ok) throw new Error('Failed to load boss history');
                const data = await res.json();
                if (!cancelled) setRuns(data);
            } catch (e) {
                console.error(e);
            } finally {
                if (!cancelled) setLoading(false);
            }
        })();
        return () => { cancelled = true; };
    }, []);

    const total = runs.length;
    const wins = runs.filter(r => r.passed).length;
    const bestScore = runs.reduce((max, r) => Math.max(max, r.score), 0);

    return (
        <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-3 text-xs font-mono text-zinc-200">
            <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                    <Trophy className="w-4 h-4 text-amber-400" />
                    <span className="text-[11px] tracking-widest uppercase text-zinc-500">
                        Boss History
                    </span>
                </div>
                {loading ? (
                    <span className="text-[10px] text-zinc-500">Loading...</span>
                ) : (
                    <span className="text-[10px] text-zinc-500">
                        {wins}/{total} cleared · Best {bestScore}
                    </span>
                )}
            </div>

            <div className="space-y-1 max-h-40 overflow-y-auto pr-1 custom-scrollbar">
                {runs.map((run, idx) => (
                    <div
                        key={`${run.boss_id}-${run.created_at}-${idx}`}
                        className="flex items-center justify-between gap-2 py-1 border-b border-zinc-800/60 last:border-b-0"
                    >
                        <div className="flex flex-col">
                            <div className="flex items-center gap-1">
                                <span className="text-[11px]">
                                    {run.passed ? '✅' : '☠️'} {run.boss_name}
                                </span>
                                <span className={`px-1.5 py-0.5 rounded text-[8px] uppercase ${run.difficulty === 'hard'
                                        ? 'bg-purple-900/50 text-purple-200'
                                        : 'bg-emerald-900/50 text-emerald-200'
                                    }`}>
                                    {run.difficulty}
                                </span>
                            </div>
                            <span className="text-[10px] text-zinc-500">
                                {new Date(run.created_at).toLocaleString()}
                            </span>
                        </div>
                        <div className="text-right">
                            <div className="text-[11px] text-cyan-300">Score {run.score}</div>
                            <div className="text-[10px] text-zinc-500">
                                INT {run.integrity_delta >= 0 ? `+${run.integrity_delta}` : run.integrity_delta}
                            </div>
                        </div>
                    </div>
                ))}

                {!loading && runs.length === 0 && (
                    <div className="text-[10px] text-zinc-500 italic py-2">
                        No raids logged yet. Trigger a boss and ship a fix.
                    </div>
                )}
            </div>
        </div>
    );
}
