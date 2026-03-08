import React, { useState, useEffect } from 'react';
import { HelpCircle, X, ChevronRight } from 'lucide-react';
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
    const [lastCoachJson, setLastCoachJson] = useState<string>('');

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

    const { recommended_hint_tier, cta } = coach;
    const failCount = cta.body?.match(/\d+/)?.[0] ?? '';

    // How many objectives are failing
    const failLabel = failCount ? `${failCount} objectives failing` : 'Some objectives failing';

    const handleDismiss = () => {
        setIsVisible(false);
        onAction('dismiss', recommended_hint_tier);
    };

    return (
        // Slim inline strip — NOT a blocking modal
        <div className={cn(
            'flex items-center gap-2 px-3 py-1.5 border-b text-xs shrink-0',
            'bg-red-950/30 border-red-900/40 text-red-300'
        )}>
            <span className="font-semibold text-red-400 shrink-0">✗ {failLabel}</span>
            <span className="text-zinc-500 truncate flex-1">{cta.body}</span>

            {/* Open Hints CTA */}
            {(cta.actions.includes('open_hint') || cta.actions.includes('unlock_hint')) && (
                <button
                    onClick={() => onAction('open_hint', recommended_hint_tier)}
                    className="flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold bg-zinc-800 border border-zinc-700 text-zinc-300 hover:text-zinc-100 hover:bg-zinc-700 transition-colors shrink-0"
                >
                    <HelpCircle className="w-3 h-3" /> Open Hints <ChevronRight className="w-3 h-3" />
                </button>
            )}

            <button onClick={handleDismiss} className="text-zinc-600 hover:text-zinc-400 shrink-0 ml-1">
                <X className="w-3.5 h-3.5" />
            </button>
        </div>
    );
}
