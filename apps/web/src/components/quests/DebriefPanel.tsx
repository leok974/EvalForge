import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, ArrowRight, Play, BookOpen, Clock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

// Interfaces based on API types
export interface DebriefData {
    title: string;
    passed_objectives: string[];
    objective_titles: { id: string; title: string }[];
    tests?: { passed: number; failed: number; mode: string };
    learning_points: string[];
    next?: {
        quest_id: string; // Slug
        title: string;
        why: string;
    } | null;
}

interface DebriefPanelProps {
    debrief: DebriefData;
    onNextQuest?: (slug: string) => void;
    onStay?: () => void;
    className?: string;
}

export function DebriefPanel({ debrief, onNextQuest, onStay, className }: DebriefPanelProps) {
    if (!debrief) return null;

    return (
        <div className={cn("flex flex-col gap-6 h-full p-6 max-w-2xl mx-auto", className)}>

            {/* Header */}
            <div className="flex items-start justify-between">
                <div>
                    <h2 className="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                        {debrief.title}
                    </h2>
                    <p className="text-zinc-400 mt-1">Excellent work! You've cleared this challenge.</p>
                </div>
                <div className="bg-emerald-500/10 p-3 rounded-full">
                    <CheckCircle className="w-8 h-8 text-emerald-400" />
                </div>
            </div>

            {/* Objectives */}
            <div className="space-y-3">
                <h3 className="text-sm font-uppercase tracking-wider text-zinc-500 font-bold">Verified Objectives</h3>
                <div className="grid gap-2">
                    {debrief.objective_titles.map((obj) => (
                        <motion.div
                            key={obj.id}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="flex items-center gap-3 bg-zinc-800/50 p-3 rounded-lg border border-zinc-700/50"
                        >
                            <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0" />
                            <span className="text-zinc-200 text-sm font-medium">{obj.title}</span>
                        </motion.div>
                    ))}
                    {/* Fallback for IDs without titles if any? Logic handled in backend but just in case */}
                    {debrief.passed_objectives
                        .filter(id => !debrief.objective_titles.find(t => t.id === id))
                        .map(id => (
                            <div key={id} className="flex items-center gap-3 bg-zinc-800/50 p-3 rounded-lg border border-zinc-700/50 opacity-80">
                                <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0" />
                                <span className="text-zinc-300 text-sm font-mono">{id}</span>
                            </div>
                        ))
                    }
                </div>
            </div>

            {/* Learning Points */}
            {debrief.learning_points.length > 0 && (
                <div className="space-y-3">
                    <h3 className="text-sm font-uppercase tracking-wider text-zinc-500 font-bold flex items-center gap-2">
                        <BookOpen className="w-4 h-4" /> Key Takeaways
                    </h3>
                    <ul className="space-y-2">
                        {debrief.learning_points.map((point, i) => (
                            <li key={i} className="flex items-start gap-3 text-zinc-300 text-sm leading-relaxed">
                                <span className="block w-1.5 h-1.5 mt-2 rounded-full bg-cyan-400 flex-shrink-0" />
                                {point}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Recommended Next Quest */}
            {debrief.next ? (
                <div className="mt-auto pt-6 border-t border-zinc-800">
                    <h3 className="text-sm font-uppercase tracking-wider text-zinc-500 font-bold mb-3 flex items-center gap-2">
                        Next Up
                    </h3>
                    <div className="bg-gradient-to-br from-indigo-900/40 to-purple-900/40 border border-indigo-500/30 rounded-xl p-4 flex flex-col sm:flex-row gap-4 items-center justify-between group cursor-pointer hover:border-indigo-500/50 transition-colors"
                        onClick={() => onNextQuest?.(debrief.next!.quest_id)}
                    >
                        <div className="flex-1">
                            <div className="text-xs text-indigo-300 font-mono mb-1">RECOMMENDED</div>
                            <div className="text-lg font-bold text-white group-hover:text-indigo-200 transition-colors">
                                {debrief.next.title}
                            </div>
                            <div className="text-sm text-zinc-400 mt-1">{debrief.next.why}</div>
                        </div>
                        <Button
                            onClick={(e) => {
                                e.stopPropagation();
                                onNextQuest?.(debrief.next!.quest_id);
                            }}
                            className="w-full sm:w-auto bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-900/20"
                        >
                            Start Quest <ArrowRight className="w-4 h-4 ml-2" />
                        </Button>
                    </div>
                </div>
            ) : (
                <div className="mt-auto pt-6 border-t border-zinc-800">
                    <div className="bg-zinc-800/50 p-4 rounded-xl text-center">
                        <h3 className="text-zinc-300 font-medium">Track Complete!</h3>
                        <p className="text-zinc-500 text-sm mt-1">You've finished all quests in this track.</p>
                        <Button variant="outline" className="mt-4" onClick={onStay}>
                            Return to Dashboard
                        </Button>
                    </div>
                </div>
            )}

            {/* Secondary Actions */}
            {debrief.next && (
                <div className="flex justify-center">
                    <button
                        onClick={onStay}
                        className="text-xs text-zinc-500 hover:text-zinc-300 transition-colors underline decoration-zinc-700 hover:decoration-zinc-500 underline-offset-4"
                    >
                        Stay on this quest for now
                    </button>
                </div>
            )}

        </div>
    );
}
