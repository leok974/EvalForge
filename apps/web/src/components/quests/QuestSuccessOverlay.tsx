import React from 'react';
import { Trophy, ArrowRight, X } from 'lucide-react';
import { QuestSummary } from '@/lib/questsApi';

interface QuestSuccessOverlayProps {
    quest: QuestSummary;
    onNext: () => void;
    onClose: () => void;
}

export function QuestSuccessOverlay({ quest, onNext, onClose }: QuestSuccessOverlayProps) {
    return (
        <div className="absolute inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-300">
            <div className="bg-zinc-900 border border-emerald-500/30 rounded-2xl shadow-2xl max-w-md w-full overflow-hidden relative animate-in zoom-in-95 duration-300">
                {/* Close Button */}
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 text-zinc-500 hover:text-zinc-300 transition-colors"
                >
                    <X className="w-5 h-5" />
                </button>

                {/* Header / Hero */}
                <div className="bg-emerald-950/30 p-8 flex flex-col items-center justify-center text-center border-b border-emerald-500/10">
                    <div className="w-16 h-16 rounded-full bg-emerald-500/20 flex items-center justify-center mb-4 shadow-[0_0_20px_rgba(16,185,129,0.3)] animate-bounce">
                        <Trophy className="w-8 h-8 text-emerald-400" />
                    </div>
                    <h2 className="text-2xl font-bold text-emerald-100 mb-1">Mission Accomplished!</h2>
                    <p className="text-emerald-400/80 text-sm font-mono uppercase tracking-widest">
                        {quest.title} Complete
                    </p>
                </div>

                {/* Body */}
                <div className="p-6 space-y-6">
                    {/* XP Reward (Simulated) */}
                    <div className="flex items-center justify-between p-4 bg-black/20 rounded-xl border border-white/5">
                        <span className="text-sm font-medium text-zinc-400">XP Earned</span>
                        <div className="flex items-center gap-2">
                            <span className="text-xl font-bold text-emerald-400">+{quest.base_xp_reward} XP</span>
                        </div>
                    </div>

                    {/* Unlocks (Mocked for now) */}
                    <div className="space-y-3">
                        <div className="flex items-center gap-3 text-sm text-zinc-300">
                            <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 shadow-[0_0_8px_rgba(34,211,238,0.5)]" />
                            <span>Codex Entry: <strong>Ignition Protocol</strong></span>
                        </div>
                    </div>

                    {/* Action */}
                    <button
                        onClick={onNext}
                        className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-black font-bold uppercase tracking-wider rounded-lg shadow-lg shadow-emerald-900/20 transition-all flex items-center justify-center gap-2 group"
                    >
                        <span>Confirm & Continue</span>
                        <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </button>
                </div>
            </div>
        </div>
    );
}
