import { useEffect, useMemo, useState } from 'react';
import { AlertTriangle, Skull, ShieldCheck, BookOpen } from 'lucide-react';
import { useBossStore } from '../store/bossStore';
import { useGameStore } from '../store/gameStore';
import { useAgentStore } from '../store/agentStore';
import { FX } from '../lib/fx';

export function BossHud() {
    const {
        activeBossId,
        bossName,
        difficulty,
        status,
        lastResult,
        integrityCurrent,
        integrityMax,
        deadlineTs,
        timeoutBoss,
        hintCodexId,
        hintUnread,
        markHintRead,
    } = useBossStore();

    const layout = useGameStore((s) => s.layout);
    const [now, setNow] = useState(() => Date.now());

    // Timer tick
    useEffect(() => {
        if (!deadlineTs || status !== 'active') return;

        const id = setInterval(() => {
            setNow(Date.now());
        }, 1000);

        return () => clearInterval(id);
    }, [deadlineTs, status]);

    // Auto-timeout when clock hits zero
    useEffect(() => {
        if (!deadlineTs || status !== 'active') return;
        if (now >= deadlineTs) {
            timeoutBoss();
            FX.emit('glitch', { intensity: 'high' });
        }
    }, [now, deadlineTs, status, timeoutBoss]);

    // Confetti on victory
    useEffect(() => {
        if (status === 'defeated') {
            FX.emit('confetti', { count: 200 });
        }
    }, [status]);

    const remainingSeconds = useMemo(() =>
        deadlineTs && status === 'active'
            ? Math.max(0, Math.floor((deadlineTs - now) / 1000))
            : 0,
        [deadlineTs, status, now]
    );

    const mmss = useMemo(() => {
        const m = Math.floor(remainingSeconds / 60);
        const s = remainingSeconds % 60;
        return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    }, [remainingSeconds]);

    const urgencyClass = useMemo(() => {
        if (status !== 'active') return 'bg-zinc-900/80 border-cyan-500/40';
        if (remainingSeconds <= 2 * 60) return 'bg-red-900/50 border-red-500/60';
        if (remainingSeconds <= 5 * 60) return 'bg-orange-900/40 border-orange-500/50';
        return 'bg-zinc-900/80 border-cyan-500/40';
    }, [status, remainingSeconds]);

    const hpPercent = (integrityCurrent / integrityMax) * 100;

    // Hide completely if nothing boss-related is happening
    if (status === 'idle' && !activeBossId && !lastResult) {
        return null;
    }

    const isWin = lastResult?.passed;

    const { openAgent } = useAgentStore();

    const handleOpenStrategy = () => {
        if (!hintCodexId) return;

        // Open Explain Agent with codex context
        openAgent('explain', { codex_id: hintCodexId }, "Help me understand how to beat this boss.");
        markHintRead();
    };

    return (
        <div className="pointer-events-none fixed top-4 inset-x-0 z-40 flex justify-center px-4">
            <div
                className={`pointer-events-auto w-full max-w-3xl rounded-2xl border ${urgencyClass} shadow-xl shadow-black/60 backdrop-blur-md p-4 space-y-3`}
            >
                {/* Header Row */}
                <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-2">
                        {status === 'defeated' ? (
                            <ShieldCheck className="w-5 h-5 text-emerald-400" />
                        ) : status === 'failed' ? (
                            <Skull className="w-5 h-5 text-red-400" />
                        ) : (
                            <AlertTriangle className="w-5 h-5 text-amber-300" />
                        )}
                        <div className="flex flex-col">
                            <div className="flex items-center gap-2">
                                <span className="text-xs uppercase tracking-[0.25em] text-zinc-400 font-mono">
                                    {activeBossId || lastResult?.boss_id || 'Boss Protocol'}
                                </span>
                                {difficulty && (
                                    <span className={`px-2 py-0.5 rounded-full text-[9px] uppercase tracking-widest ${difficulty === 'hard'
                                        ? 'bg-purple-900/70 text-purple-200'
                                        : 'bg-emerald-900/70 text-emerald-200'
                                        }`}>
                                        {difficulty}
                                    </span>
                                )}
                            </div>
                            <span className="text-sm text-zinc-200 font-mono">
                                {bossName || (status === 'active'
                                    ? 'Reactor Core Meltdown – Contain the breach.'
                                    : status === 'defeated'
                                        ? 'Boss defeated. Systems stabilizing.'
                                        : status === 'failed'
                                            ? 'Boss escaped. Integrity compromised.'
                                            : 'Boss encounter resolved.')}
                            </span>
                        </div>
                    </div>

                    <div className="flex items-center gap-2">
                        {/* Strategy Guide Button */}
                        {hintCodexId && (
                            <button
                                onClick={handleOpenStrategy}
                                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-[11px] font-mono transition-colors ${hintUnread
                                    ? 'border-amber-400/60 bg-amber-950/40 text-amber-200 hover:bg-amber-900/60'
                                    : 'border-cyan-400/40 bg-cyan-950/30 text-cyan-200 hover:bg-cyan-900/50'
                                    }`}
                                title="Open strategy guide in codex"
                            >
                                <BookOpen className="w-3.5 h-3.5" />
                                Strategy Guide
                                {hintUnread && (
                                    <span className="ml-0.5 inline-flex w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
                                )}
                            </button>
                        )}

                        {/* Timer */}
                        {status === 'active' && deadlineTs && (
                            <div className="flex items-center gap-2 bg-black/40 rounded-full px-3 py-1 border border-red-600/40">
                                <span className="text-[10px] font-mono text-red-300">
                                    MELTDOWN TIMER
                                </span>
                                <span className="text-sm font-mono text-red-100 tabular-nums">
                                    {mmss}
                                </span>
                            </div>
                        )}
                    </div>
                </div>

                {/* HP Bar + Score */}
                <div className="flex flex-col md:flex-row gap-3 md:items-center">
                    {/* HP Bar */}
                    <div className="flex-1">
                        <div className="flex justify-between text-[10px] text-zinc-400 font-mono mb-1">
                            <span>SYSTEM INTEGRITY</span>
                            <span>
                                {integrityCurrent}/{integrityMax}
                            </span>
                        </div>
                        <div className="w-full h-3 rounded-full bg-zinc-900 overflow-hidden border border-zinc-700/80">
                            <div
                                className={`h-full transition-all duration-500 ${hpPercent > 60
                                    ? 'bg-emerald-400'
                                    : hpPercent > 30
                                        ? 'bg-amber-400'
                                        : 'bg-red-500'
                                    }`}
                                style={{ width: `${Math.max(0, Math.min(100, hpPercent))}%` }}
                            />
                        </div>
                    </div>

                    {/* Score / Outcome */}
                    {lastResult && (
                        <div className="md:w-40 flex flex-col items-end gap-1">
                            <span className="text-[10px] font-mono text-zinc-400">
                                BOSS SCORE
                            </span>
                            <span
                                className={`text-lg font-mono ${isWin ? 'text-emerald-300' : 'text-red-300'
                                    }`}
                            >
                                {lastResult.score}
                            </span>
                            <span className="text-[10px] font-mono text-zinc-500">
                                {isWin ? 'DEFEATED' : 'FAILED'}
                            </span>
                        </div>
                    )}
                </div>

                {/* Breakdown (optional, compact) */}
                {lastResult?.breakdown && (
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-1 text-[10px] text-zinc-400 font-mono mt-1">
                        {Object.entries(lastResult.breakdown).map(([k, v]) => (
                            <div key={k} className="flex justify-between">
                                <span className="truncate">{k}</span>
                                <span className="text-zinc-200 ml-2">{v}</span>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
