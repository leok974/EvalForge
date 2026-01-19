import React, { useState } from 'react';
import { X } from 'lucide-react';
import { QuestSummary } from '@/lib/questsApi';
import { DebriefPanel, DebriefData } from './DebriefPanel';

interface QuestSuccessOverlayProps {
    quest: QuestSummary;
    debrief?: DebriefData; // Optional now
    onNext: (questId?: string) => void;
    onClose: () => void;
}

export function QuestSuccessOverlay({ quest, debrief, onNext, onClose }: QuestSuccessOverlayProps) {

    // If we have debrief data, use the panel
    if (debrief) {
        return (
            <div className="absolute inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 animate-in fade-in duration-300">
                <div className="bg-zinc-900 border border-zinc-800 rounded-2xl shadow-2xl max-w-2xl w-full h-[80vh] overflow-auto relative animate-in zoom-in-95 duration-300 flex flex-col">
                    <button
                        onClick={onClose}
                        className="absolute top-4 right-4 text-zinc-500 hover:text-zinc-300 transition-colors z-10"
                    >
                        <X className="w-5 h-5" />
                    </button>
                    <DebriefPanel
                        debrief={debrief}
                        onNextQuest={(slug) => onNext(slug)}
                        onStay={onClose}
                    />
                </div>
            </div>
        );
    }

    // Fallback Legacy UI (Simulated rewards)
    return (
        <div className="absolute inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-300">
            <div className="bg-zinc-900 border border-emerald-500/30 rounded-2xl shadow-2xl max-w-md w-full overflow-hidden relative animate-in zoom-in-95 duration-300">
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 text-zinc-500 hover:text-zinc-300 transition-colors"
                >
                    <X className="w-5 h-5" />
                </button>

                <div className="bg-emerald-950/30 p-8 flex flex-col items-center justify-center text-center border-b border-emerald-500/10">
                    <div className="w-16 h-16 rounded-full bg-emerald-500/20 flex items-center justify-center mb-4 shadow-[0_0_20px_rgba(16,185,129,0.3)] animate-bounce">
                        <span className="text-2xl">🏆</span>
                    </div>
                    <h2 className="text-2xl font-bold text-emerald-100 mb-1">Mission Accomplished!</h2>
                    <p className="text-emerald-400/80 text-sm font-mono uppercase tracking-widest">
                        {quest.title} Complete
                    </p>
                </div>

                <div className="p-6 space-y-6">
                    <div className="flex items-center justify-between p-4 bg-black/20 rounded-xl border border-white/5">
                        <span className="text-sm font-medium text-zinc-400">XP Earned</span>
                        <div className="flex items-center gap-2">
                            <span className="text-xl font-bold text-emerald-400">+{quest.base_xp_reward} XP</span>
                        </div>
                    </div>

                    <button
                        onClick={() => onNext()}
                        className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-black font-bold uppercase tracking-wider rounded-lg shadow-lg shadow-emerald-900/20 transition-all flex items-center justify-center gap-2 group"
                    >
                        <span>Confirm & Continue</span>
                    </button>
                </div>
            </div>
        </div>
    );
}
