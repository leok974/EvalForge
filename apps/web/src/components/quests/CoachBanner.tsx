import React, { useState, useEffect } from 'react';
import { Lightbulb, Key, X, GraduationCap, AlertTriangle } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface CoachData {
    stuck_level: number;
    reason: string;
    recommended_hint_tier: 'concept' | 'guided' | 'full_solution';
    cta: {
        title: string;
        body: string;
        actions: string[];
    };
}

interface CoachBannerProps {
    coach: CoachData | null;
    onAction: (action: string, tier: string) => void;
}

export function CoachBanner({ coach, onAction }: CoachBannerProps) {
    const [isVisible, setIsVisible] = useState(false);
    const [lastCoachJson, setLastCoachJson] = useState<string>("");

    useEffect(() => {
        if (coach) {
            const json = JSON.stringify(coach);
            if (json !== lastCoachJson) {
                setIsVisible(true);
                setLastCoachJson(json);
            }
        } else {
            setIsVisible(false);
        }
    }, [coach, lastCoachJson]);

    if (!coach || !isVisible) return null;

    const { stuck_level, recommended_hint_tier, cta } = coach;

    const handleDismiss = () => {
        setIsVisible(false);
        onAction('dismiss', recommended_hint_tier);
    };

    const isConcept = recommended_hint_tier === 'concept';
    const isGuided = recommended_hint_tier === 'guided';
    const isSolution = recommended_hint_tier === 'full_solution';

    return (
        <div className={cn(
            "p-3 mx-4 mb-2 rounded-lg border flex items-start gap-4 shadow-lg animate-in slide-in-from-top-2 duration-300 relative overflow-hidden",
            stuck_level >= 3 ? "bg-amber-950/40 border-amber-500/50" :
                stuck_level === 2 ? "bg-blue-950/40 border-blue-500/50" :
                    "bg-zinc-900/80 border-zinc-700"
        )}>
            {/* Background Glow */}
            <div className={cn(
                "absolute top-0 right-0 w-64 h-64 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 opacity-20 pointer-events-none",
                stuck_level >= 3 ? "bg-amber-500" : "bg-blue-500"
            )} />

            {/* Icon */}
            <div className={cn(
                "p-2 rounded-full shrink-0 border",
                stuck_level >= 3 ? "bg-amber-500/10 border-amber-500/30 text-amber-400" : "bg-blue-500/10 border-blue-500/30 text-blue-400"
            )}>
                {stuck_level >= 3 ? <AlertTriangle className="w-5 h-5" /> : <GraduationCap className="w-5 h-5" />}
            </div>

            {/* Content */}
            <div className="flex-1 min-w-0 z-10">
                <h4 className={cn(
                    "text-sm font-bold uppercase tracking-wide mb-1 flex items-center gap-2",
                    stuck_level >= 3 ? "text-amber-400" : "text-blue-300"
                )}>
                    {cta.title}
                    <span className="text-[9px] px-1.5 py-0.5 rounded-full bg-black/30 border border-white/10 opacity-70">
                        Level {stuck_level}
                    </span>
                </h4>
                <p className="text-xs text-zinc-300 leading-relaxed max-w-prose">
                    {cta.body}
                </p>

                {/* Actions */}
                <div className="flex items-center gap-2 mt-3">
                    {cta.actions.includes("open_hint") && (
                        <button
                            onClick={() => onAction('open_hint', recommended_hint_tier)}
                            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded flex items-center gap-1.5 transition-colors shadow-sm"
                        >
                            <Lightbulb className="w-3.5 h-3.5" />
                            View Hint
                        </button>
                    )}

                    {cta.actions.includes("unlock_hint") && !cta.actions.includes("open_hint") && (
                        <button
                            onClick={() => onAction('unlock_hint', recommended_hint_tier)}
                            className="px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-600 hover:border-zinc-500 text-xs font-bold rounded flex items-center gap-1.5 transition-all"
                        >
                            <Key className="w-3.5 h-3.5" />
                            Unlock {isConcept ? "Concept" : isGuided ? "Guide" : "Solution"}
                        </button>
                    )}

                    <button
                        onClick={handleDismiss}
                        className="px-3 py-1.5 text-zinc-500 hover:text-zinc-300 text-xs font-medium transition-colors"
                    >
                        Dismiss
                    </button>
                </div>
            </div>

            {/* Close X */}
            <button
                onClick={handleDismiss}
                className="text-zinc-600 hover:text-white transition-colors"
            >
                <X className="w-4 h-4" />
            </button>
        </div>
    );
}
