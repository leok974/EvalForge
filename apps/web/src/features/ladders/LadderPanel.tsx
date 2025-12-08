import { useEffect, useState } from "react";
import { LadderSpec } from "./types";
import { cn } from "@/lib/utils";
import { CheckCircle2, Lock, Unlock } from "lucide-react";

interface LadderPanelProps {
    worldSlug: string;
    className?: string;
}

export function LadderPanel({ worldSlug, className }: LadderPanelProps) {
    const [ladder, setLadder] = useState<LadderSpec | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Mock progress state for now (would come from store)
    // assuming stage 1 passed if bosses killed etc.
    // For MVP just rendering the structure
    const currentStageIndex = 0; // mocked

    useEffect(() => {
        if (!worldSlug) {
            setLadder(null);
            return;
        }

        async function fetchLadder() {
            setLoading(true);
            setError(null);
            try {
                const res = await fetch(`/api/worlds/${worldSlug}/ladder`);
                if (!res.ok) throw new Error("Ladder not found");
                const data = await res.json();
                setLadder(data);
            } catch (err) {
                console.warn(err);
                setError("No ladder available");
            } finally {
                setLoading(false);
            }
        }

        fetchLadder();
    }, [worldSlug]);

    if (!ladder) {
        if (loading) return <div className="text-xs text-slate-500 animate-pulse">Loading ladder...</div>;
        return null; // Don't render if no ladder
    }

    return (
        <div className={cn("flex flex-col gap-4 p-4 rounded-xl border border-slate-800 bg-slate-900/50", className)}>
            <div>
                <h3 className="text-sm font-bold text-cyan-300 tracking-wide uppercase">{ladder.title}</h3>
                <p className="text-xs text-slate-400 mt-1 leading-relaxed">{ladder.summary}</p>
            </div>

            <div className="flex flex-col gap-3 relative">
                {/* Connector Line */}
                <div className="absolute left-[15px] top-4 bottom-4 w-0.5 bg-slate-800" />

                {ladder.stages.map((stage, idx) => {
                    const isLocked = idx > currentStageIndex;
                    const isCompleted = idx < currentStageIndex;
                    const isActive = idx === currentStageIndex;

                    return (
                        <div key={stage.stage_id} className="relative pl-10">
                            {/* Node Indicator */}
                            <div className={cn(
                                "absolute left-0 top-1 w-8 h-8 rounded-full border-2 flex items-center justify-center z-10 bg-slate-950",
                                isActive ? "border-cyan-400 text-cyan-400" :
                                    isCompleted ? "border-emerald-500 text-emerald-500" :
                                        "border-slate-700 text-slate-700"
                            )}>
                                {isCompleted ? <CheckCircle2 size={14} /> :
                                    isLocked ? <Lock size={12} /> :
                                        <div className="text-[10px] font-bold">{idx + 1}</div>}
                            </div>

                            <div className={cn(
                                "p-3 rounded-lg border",
                                isActive ? "border-cyan-500/30 bg-cyan-500/5" :
                                    isLocked ? "border-slate-800 bg-slate-950/50 opacity-60" :
                                        "border-emerald-500/20 bg-emerald-500/5"
                            )}>
                                <div className="flex justify-between items-start mb-2">
                                    <span className={cn("text-xs font-semibold", isActive ? "text-cyan-100" : "text-slate-300")}>
                                        {stage.title}
                                    </span>
                                    {stage.badge && (
                                        <span className="text-[9px] px-1.5 py-0.5 rounded border border-slate-700 text-slate-500">
                                            {stage.badge.label}
                                        </span>
                                    )}
                                </div>
                                <div className="text-[10px] text-slate-400 mb-2">
                                    {stage.description}
                                </div>

                                {/* Nodes List (New System) or Legacy Dots */}
                                {stage.nodes ? (
                                    <div className="flex flex-col gap-2 mt-2">
                                        {stage.nodes.map(node => {
                                            const isLegendary = node.kind === "legendary_boss" || (node as any).legendary_boss === true;
                                            return (
                                                <div
                                                    key={node.id}
                                                    data-testid={`ladder-node-${isLegendary ? 'legendary' : 'normal'}-${node.id}`}
                                                    className={cn(
                                                        "rounded-md border px-3 py-2 text-xs transition flex items-center justify-between",
                                                        isLegendary
                                                            ? "border-amber-400/80 bg-amber-950/50 shadow-[0_0_12px_rgba(251,191,36,0.45)]"
                                                            : "border-emerald-500/20 bg-emerald-950/20"
                                                    )}
                                                >
                                                    <div className="flex items-center gap-2">
                                                        <span>{node.label}</span>
                                                        {isLegendary && (
                                                            <span className="text-[9px] font-semibold uppercase tracking-wide text-amber-200 animate-pulse">
                                                                Legendary
                                                            </span>
                                                        )}
                                                    </div>
                                                </div>
                                            );
                                        })}
                                    </div>
                                ) : (
                                    <div className="flex flex-wrap gap-1.5">
                                        {stage.quests.map(q => (
                                            <div key={q} className="w-1.5 h-1.5 rounded-full bg-slate-700 hover:bg-slate-500 transition-colors cursor-help" title={q} />
                                        ))}
                                        {stage.bosses.map(b => (
                                            <div key={b} className="w-2 h-2 rounded-sm bg-rose-500/70 hover:bg-rose-400 transition-colors cursor-help" title={b} />
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    );
                })}
            </div>

            <div className="mt-2 pt-3 border-t border-slate-800 flex items-center gap-2 text-[10px] text-slate-500">
                <Unlock size={10} />
                <span>Complete all stages to earn: <span className="text-cyan-400">{ladder.completion_rewards.titles[0]}</span></span>
            </div>
        </div>
    );
}
