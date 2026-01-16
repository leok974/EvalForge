import React, { useState } from 'react';
import { cn } from '@/lib/utils';
import { FileText, ListChecks, Scroll, Library, HelpCircle, ChevronUp, Lock } from 'lucide-react';
import { QuestSummary } from '@/lib/questsApi';
import ReactMarkdown from 'react-markdown';

interface QuestDrawerProps {
    quest: QuestSummary;
    objectivesState: Record<string, boolean>; // id -> ok
    onObjectiveClick: (objectiveId: string) => void;
}

type Tab = 'briefing' | 'objectives' | 'lore' | 'hints';

export function QuestDrawer({ quest, objectivesState, onObjectiveClick }: QuestDrawerProps) {
    const [activeTab, setActiveTab] = useState<Tab>('briefing');

    // Simple verification for "Unlockable" hints (mocked for now)
    const [unlockedHints, setUnlockedHints] = useState<Record<string, boolean>>({});

    const toggleHint = async (id: string, type: 'concept' | 'snippet' | 'solution') => {
        // If already unlocked locally, just toggle visibility (mock logic implied toggle meant "unlock")
        // But UI structure assumes toggle = expand. 
        // Let's assume click = "Unlock and Expand".

        if (unlockedHints[id]) {
            // If already unlocked, maybe we just want to toggle visibility? 
            // The current UI just renders content if unlockedHints[id] is true.
            // So "toggle" essentially means "toggle unlock status" in the mock.
            // In real app, once unlocked, it stays unlocked.
            return;
        }

        try {
            const { unlockHint } = await import('@/lib/questsApi');
            // Map type to tier? 
            // concept=1, snippet=2, solution=3
            const tierMap = { concept: 1, snippet: 2, solution: 3 };
            const tier = tierMap[type];

            const res = await unlockHint(quest.slug, tier);
            if (res.ok) {
                setUnlockedHints(prev => ({ ...prev, [id]: true }));
            } else {
                // Show error toast or shake? For now console warn
                console.warn("Hint unlock failed:", res.reason);
                alert(`Locked: ${res.reason}`);
            }
        } catch (e) {
            console.error(e);
        }
    };

    const tabs: { id: Tab; label: string; icon: any }[] = [
        { id: 'briefing', label: 'Briefing', icon: FileText },
        { id: 'objectives', label: 'Objectives', icon: ListChecks },
        { id: 'hints', label: 'Hints', icon: HelpCircle },
        { id: 'lore', label: 'Lore', icon: Scroll },
    ];

    return (
        <div className="h-full flex flex-col bg-zinc-950/50">
            {/* Tabs Header */}
            <div className="flex items-center border-b border-zinc-800 bg-zinc-900/40">
                {tabs.map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={cn(
                            "flex-1 flex items-center justify-center gap-2 py-3 text-[10px] font-bold uppercase tracking-wider transition-all border-b-2",
                            activeTab === tab.id
                                ? "text-cyan-400 border-cyan-500 bg-cyan-950/10"
                                : "text-zinc-500 border-transparent hover:text-zinc-300 hover:bg-zinc-900"
                        )}
                    >
                        <tab.icon className="w-3 h-3" />
                        <span className="hidden xl:inline">{tab.label}</span>
                    </button>
                ))}
            </div>

            {/* Content Area */}
            <div className="flex-1 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-zinc-800 scrollbar-track-transparent">

                {/* BRIEFING TAB */}
                {activeTab === 'briefing' && (
                    <div className="space-y-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
                        <div className="prose prose-invert prose-sm max-w-none prose-p:text-zinc-300 prose-headings:text-cyan-100 prose-strong:text-cyan-200">
                            <ReactMarkdown>{quest.briefing_md || "*Encrypted Transmission...*"}</ReactMarkdown>
                        </div>
                    </div>
                )}

                {/* OBJECTIVES TAB */}
                {activeTab === 'objectives' && (
                    <div className="space-y-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
                        <h4 className="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-2">Success Criteria</h4>
                        <div className="space-y-2">
                            {quest.objectives?.map((obj) => (
                                <button
                                    key={obj.id}
                                    onClick={() => onObjectiveClick?.(obj.id)}
                                    className={cn(
                                        "w-full text-left p-3 rounded-lg border group transition-all hover:bg-zinc-900/60 relative overflow-hidden",
                                        objectivesState[obj.id]
                                            ? "bg-emerald-950/20 border-emerald-500/30"
                                            : "bg-zinc-950/40 border-zinc-800 hover:border-zinc-700"
                                    )}
                                >
                                    {/* Pulse effect on hover */}
                                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent opacity-0 group-hover:opacity-100 -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />

                                    <div className="flex items-start gap-3 relative z-10">
                                        <div className={cn(
                                            "mt-0.5 w-4 h-4 rounded-full border flex items-center justify-center shrink-0 transition-colors",
                                            objectivesState[obj.id]
                                                ? "bg-emerald-500 border-emerald-400 text-black shadow-[0_0_10px_rgba(16,185,129,0.4)]"
                                                : "border-zinc-700 group-hover:border-zinc-500"
                                        )}>
                                            {objectivesState[obj.id] && "✓"}
                                        </div>
                                        <div>
                                            <span className={cn(
                                                "text-xs font-mono block mb-0.5",
                                                objectivesState[obj.id] ? "text-emerald-200" : "text-zinc-300 group-hover:text-zinc-100"
                                            )}>
                                                {obj.text}
                                            </span>
                                            {obj.why && (
                                                <span className="text-[10px] text-zinc-500 block leading-tight">
                                                    {obj.why}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                </button>
                            ))}
                            {!quest.objectives?.length && (
                                <div className="text-xs text-zinc-500 italic">No specific objectives listed.</div>
                            )}
                        </div>
                    </div>
                )}

                {/* HINTS TAB */}
                {activeTab === 'hints' && (
                    <div className="space-y-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
                        <h4 className="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-2">Field Manual</h4>

                        <div className="space-y-3">
                            {quest.hints?.map((hint) => (
                                <div key={hint.id} className="border border-zinc-800 rounded-lg overflow-hidden bg-zinc-900/20">
                                    <button
                                        onClick={() => toggleHint(hint.id, hint.type)}
                                        className="w-full flex items-center justify-between p-3 text-left hover:bg-zinc-800/50 transition-colors"
                                    >
                                        <div className="flex items-center gap-2">
                                            {hint.type === 'concept' && <div className="text-[10px] bg-blue-900/30 text-blue-400 px-2 py-0.5 rounded border border-blue-500/20 uppercase tracking-wide">Concept</div>}
                                            {hint.type === 'snippet' && <div className="text-[10px] bg-amber-900/30 text-amber-400 px-2 py-0.5 rounded border border-amber-500/20 uppercase tracking-wide">Snippet</div>}
                                            {hint.type === 'solution' && <div className="text-[10px] bg-red-900/30 text-red-400 px-2 py-0.5 rounded border border-red-500/20 uppercase tracking-wide">Solution</div>}
                                            <span className="text-xs text-zinc-400 font-mono">
                                                {unlockedHints[hint.id] ? "Access Granted" : "Encrypted Data"}
                                            </span>
                                        </div>
                                        <div className="text-zinc-600">
                                            {unlockedHints[hint.id] ? <ChevronUp className="w-4 h-4" /> : <div className="flex items-center gap-1 text-[10px] uppercase font-bold text-zinc-600"><Lock className="w-3 h-3" /> Unlock</div>}
                                        </div>
                                    </button>

                                    {unlockedHints[hint.id] && (
                                        <div className="p-3 border-t border-zinc-800/50 bg-black/20 animate-in slide-in-from-top-2">
                                            <div className="text-sm text-zinc-300 font-mono whitespace-pre-wrap">
                                                <ReactMarkdown>{hint.text}</ReactMarkdown>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            ))}
                            {!quest.hints?.length && (
                                <div className="text-zinc-500 italic text-xs text-center py-8">
                                    No hints available for this mission.
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {/* LORE TAB */}
                {activeTab === 'lore' && (
                    <div className="space-y-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
                        <div className="p-4 rounded-lg border border-amber-900/20 bg-amber-950/5 relative overflow-hidden">
                            <div className="absolute top-0 right-0 p-2 opacity-50">
                                <Library className="w-8 h-8 text-amber-900/20" />
                            </div>
                            <h4 className="text-xs font-bold uppercase tracking-widest text-amber-600 mb-3">Codex Entry</h4>
                            <div className="prose prose-invert prose-sm max-w-none prose-p:text-amber-100/60 prose-blockquote:border-amber-900/50 prose-blockquote:bg-amber-950/10 prose-blockquote:text-amber-200/80 italic font-serif">
                                <ReactMarkdown>{quest.lore_md || "> *Data corrupted...*"}</ReactMarkdown>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
