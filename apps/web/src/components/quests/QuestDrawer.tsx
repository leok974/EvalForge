import React, { useState, useEffect } from 'react';
import { cn } from '@/lib/utils';
import { FileText, ListChecks, Scroll, Library, HelpCircle, ChevronUp, ChevronDown, Lock, History, Check, X, Clock, GraduationCap, Database } from 'lucide-react';
import { QuestSummary, QuestAttemptSummary } from '@/lib/questsApi';
import ReactMarkdown from 'react-markdown';

// Parse a hints.md file with "## Hint N — title" sections into structured accordion data
function parseHints(md: string): { intro: string; hints: { title: string; body: string }[] } {
    const parts = md.split(/\n(?=##\s)/);
    const introPart = parts[0] ?? '';
    const intro = introPart.replace(/^#[^\n]*\n/, '').trim(); // strip h1 title
    const hints = parts.slice(1).map(chunk => {
        const [rawTitle, ...rest] = chunk.split('\n');
        return {
            title: rawTitle.replace(/^##\s+/, '').trim(),
            body: rest.join('\n').trim(),
        };
    });
    return { intro, hints };
}

interface QuestDrawerProps {
    quest: QuestSummary;
    objectivesState: Record<string, boolean>; // id -> ok
    onObjectiveClick: (objectiveId: string) => void;
    // New History Props
    attempts?: QuestAttemptSummary[];
    onSelectAttempt?: (attemptId: string) => void;
    // Tab Control
    controlTab?: Tab; // 'briefing' | 'objectives' | 'lore' | 'hints' | 'history' | 'tutorial'
    onTabChange?: (tab: Tab) => void;
    // Phase 9.1: Custom Panels (Tutorial)
    customPanels?: {
        tutorial?: React.ReactNode;
        database?: React.ReactNode;
    };
}

type Tab = 'briefing' | 'objectives' | 'lore' | 'hints' | 'history' | 'tutorial' | 'database';

export function QuestDrawer({ quest, objectivesState, onObjectiveClick, attempts = [], onSelectAttempt, controlTab, onTabChange, customPanels }: QuestDrawerProps) {
    const [activeTab, setActiveTab] = useState<Tab>('briefing');

    // Sync external control
    useEffect(() => {
        if (controlTab) {
            setActiveTab(controlTab);
        }
    }, [controlTab]);

    // Internal handler to notify parent
    const handleTabClick = (tab: Tab) => {
        setActiveTab(tab);
        onTabChange?.(tab);
    };

    // Simple verification for "Unlockable" hints (mocked for now)
    const [unlockedHints, setUnlockedHints] = useState<Record<string, boolean>>({});
    // Accordion index for hints_md mode
    const [openHintIdx, setOpenHintIdx] = useState<number | null>(null);
    // Gated unlock count — persisted per quest in localStorage
    const hintsKey = `hints:unlocked:${quest.slug}`;
    const [unlockedCount, setUnlockedCount] = useState(() => {
        const v = Number(localStorage.getItem(`hints:unlocked:${quest.slug}`));
        return Number.isFinite(v) && v > 0 ? v : 1;
    });
    useEffect(() => {
        localStorage.setItem(hintsKey, String(unlockedCount));
    }, [hintsKey, unlockedCount]);

    // Init unlocked hints from quest prop if available (Backend 7.1)
    useEffect(() => {
        if ((quest as any).hint_tier_unlocked > 0) {
            const tier = (quest as any).hint_tier_unlocked;
            // Map tier to unlock map
            const map: Record<string, boolean> = {};
            quest.hints?.forEach(h => {
                // Heuristic: map type to tier
                const hTier = h.type === 'concept' ? 1 : h.type === 'snippet' ? 2 : 3;
                if (hTier <= tier) map[h.id] = true;
            });
            setUnlockedHints(prev => ({ ...prev, ...map }));
        }
    }, [quest]);

    const toggleHint = async (id: string, type: 'concept' | 'snippet' | 'solution') => {
        // ... (existing hint logic)
        if (unlockedHints[id]) return;

        try {
            const { unlockHint } = await import('@/lib/questsApi');
            const tierMap = { concept: 1, snippet: 2, solution: 3 };
            const tier = tierMap[type];

            const res = await unlockHint(quest.slug, tier);
            if (res.ok) {
                setUnlockedHints(prev => ({ ...prev, [id]: true }));
            } else {
                console.warn("Hint unlock failed:", res.reason);
                alert(`Locked: ${res.reason}`);
            }
        } catch (e) {
            console.error(e);
        }
    };

    const tabs: { id: Tab; label: string; icon: any }[] = [
        // Phase 9.1: Tutorial Tab (First if available)
        ...(customPanels?.tutorial ? [{ id: 'tutorial' as Tab, label: 'Tutorial', icon: GraduationCap }] : []),
        { id: 'briefing', label: 'Briefing', icon: FileText },
        { id: 'objectives', label: 'Objectives', icon: ListChecks },
        { id: 'hints', label: 'Hints', icon: HelpCircle },
        // Phase 9.2: Database Tab
        ...(customPanels?.database ? [{ id: 'database' as Tab, label: 'Database', icon: Database }] : []),
        { id: 'history', label: 'History', icon: History },
        { id: 'lore', label: 'Lore', icon: Scroll },
    ];

    return (
        <div className="flex-1 min-h-0 min-w-0 flex flex-col bg-zinc-950/50">
            {/* Tabs Header */}
            <div className="shrink-0 min-h-[40px] flex items-center border-b border-zinc-800 bg-zinc-900/40 overflow-x-auto scrollbar-hide">
                {tabs.map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => handleTabClick(tab.id)}
                        className={cn(
                            "flex-none flex items-center justify-center gap-2 py-2 px-2 leading-none text-[10px] font-bold uppercase tracking-wider transition-all border-b-2 min-w-[80px]",
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
            <div className="flex-1 min-h-0 min-w-0 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-zinc-800 scrollbar-track-transparent">

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
                                                {/* Belt-and-suspenders: text (normalised) || title (raw DB) || visible placeholder */}
                                                {(obj as any).text || (obj as any).title || <span className="opacity-40 italic">(missing objective text)</span>}
                                                {/* Dev-visible kind badge: helps catch future shape drift before it silences rows */}
                                                {import.meta.env.DEV && !(obj as any).text && (
                                                    <span className="ml-1 text-[9px] text-amber-500 font-mono">[no text — kind: {(obj as any).kind ?? obj.validator?.kind ?? '?'}]</span>
                                                )}
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

                {/* HISTORY TAB */}
                {activeTab === 'history' && (
                    <div className="space-y-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
                        <h4 className="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-2">Run History</h4>
                        <div className="space-y-2">
                            {attempts.map((attempt) => (
                                <button
                                    key={attempt.id}
                                    onClick={() => onSelectAttempt?.(attempt.id)}
                                    className="w-full text-left p-3 rounded-lg border border-zinc-800 bg-zinc-900/20 hover:bg-zinc-800/40 hover:border-zinc-700 transition-all group"
                                >
                                    <div className="flex items-center justify-between mb-1">
                                        <span className={cn(
                                            "text-xs font-bold uppercase tracking-wide",
                                            attempt.passed ? "text-emerald-400" : "text-amber-400"
                                        )}>
                                            Run #{attempt.run_number}
                                        </span>
                                        <span className="text-[10px] text-zinc-600 font-mono">
                                            {new Date(attempt.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </span>
                                    </div>
                                    <div className="flex items-center gap-3 text-[10px] text-zinc-500">
                                        <span className="flex items-center gap-1">
                                            {attempt.passed ? <Check className="w-3 h-3" /> : <X className="w-3 h-3" />}
                                            {attempt.passed ? "Passed" : "Failed"}
                                        </span>
                                        <span className="flex items-center gap-1">
                                            <Clock className="w-3 h-3" />
                                            {attempt.duration_ms}ms
                                        </span>
                                        {attempt.is_submit && <span className="text-cyan-500 font-bold ml-auto">SUBMIT</span>}
                                    </div>
                                </button>
                            ))}
                            {!attempts.length && (
                                <div className="text-zinc-500 italic text-xs text-center py-8">
                                    No runs recorded yet.
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {/* HINTS TAB — accordion + gated unlock */}
                {activeTab === 'hints' && (() => {
                    const hintsMd = (quest as any).hints_md as string | undefined;
                    if (hintsMd) {
                        const { intro, hints } = parseHints(hintsMd);
                        const total = hints.length;
                        const allUnlocked = unlockedCount >= total;

                        function unlockNext() {
                            const next = Math.min(total, unlockedCount + 1);
                            setUnlockedCount(next);
                            setOpenHintIdx(next - 1); // auto-open the newly unlocked hint
                        }

                        const unlockLabel = unlockedCount === 1
                            ? 'I need a hint'
                            : allUnlocked
                                ? 'All hints unlocked'
                                : 'One more hint, please';

                        return (
                            <div className="space-y-3 animate-in fade-in slide-in-from-bottom-2 duration-300">
                                {intro && (
                                    <div className="prose prose-invert prose-sm max-w-none prose-p:text-zinc-400 mb-1">
                                        <ReactMarkdown>{intro}</ReactMarkdown>
                                    </div>
                                )}

                                {/* Unlock progress + button */}
                                <div className="flex items-center justify-between gap-3 py-1">
                                    <span className="text-[10px] text-zinc-600 tabular-nums">
                                        {unlockedCount}/{total} hints available
                                    </span>
                                    <button
                                        disabled={allUnlocked}
                                        onClick={unlockNext}
                                        className="flex items-center gap-1.5 px-3 py-1 rounded-md text-[11px] font-semibold border transition-all
                                            bg-cyan-600/15 text-cyan-300 border-cyan-700/40 hover:bg-cyan-600/25
                                            disabled:opacity-35 disabled:cursor-not-allowed disabled:hover:bg-cyan-600/15"
                                    >
                                        {!allUnlocked && <HelpCircle className="w-3 h-3" />}
                                        {unlockLabel}
                                    </button>
                                </div>

                                {/* Hint cards */}
                                {hints.map((h, idx) => {
                                    const isUnlocked = idx < unlockedCount;
                                    const isOpen = openHintIdx === idx && isUnlocked;
                                    return (
                                        <div
                                            key={idx}
                                            className={cn(
                                                'border rounded-lg overflow-hidden transition-opacity',
                                                isUnlocked ? 'border-zinc-800 bg-zinc-900/20' : 'border-zinc-900 bg-zinc-950/40 opacity-50'
                                            )}
                                        >
                                            <button
                                                disabled={!isUnlocked}
                                                onClick={() => setOpenHintIdx(isOpen ? null : idx)}
                                                title={!isUnlocked ? 'Unlock this hint to view it.' : undefined}
                                                className={cn(
                                                    'w-full flex items-center justify-between px-3 py-2.5 text-left transition-colors group',
                                                    isUnlocked ? 'hover:bg-zinc-800/50 cursor-pointer' : 'cursor-not-allowed'
                                                )}
                                            >
                                                <div className="flex items-center gap-2 min-w-0">
                                                    {isUnlocked
                                                        ? <span className="text-[10px] font-bold text-cyan-600 tabular-nums shrink-0">{String(idx + 1).padStart(2, '0')}</span>
                                                        : <Lock className="w-3 h-3 text-zinc-600 shrink-0" />
                                                    }
                                                    <span className={cn(
                                                        'text-xs font-semibold truncate',
                                                        isUnlocked ? 'text-zinc-300 group-hover:text-zinc-100' : 'text-zinc-600'
                                                    )}>
                                                        {h.title}
                                                    </span>
                                                </div>
                                                {isUnlocked && (
                                                    isOpen
                                                        ? <ChevronUp className="w-3.5 h-3.5 text-zinc-500 shrink-0" />
                                                        : <ChevronDown className="w-3.5 h-3.5 text-zinc-600 shrink-0" />
                                                )}
                                            </button>
                                            {isOpen && (
                                                <div className="px-4 pb-4 pt-1 border-t border-zinc-800/50 bg-black/20 animate-in slide-in-from-top-1 duration-150">
                                                    <div className="prose prose-invert prose-sm max-w-none prose-p:text-zinc-300 prose-strong:text-cyan-200 prose-code:text-amber-300 prose-code:bg-zinc-800/60 prose-code:px-1 prose-code:rounded prose-li:text-zinc-300">
                                                        <ReactMarkdown>{h.body}</ReactMarkdown>
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    );
                                })}
                            </div>
                        );
                    }
                    if (quest.hints?.length) {
                        return (
                            <div className="space-y-3 animate-in fade-in slide-in-from-bottom-2 duration-300">
                                <h4 className="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-2">Field Manual</h4>
                                {quest.hints.map((hint) => (
                                    <div key={hint.id} className="border border-zinc-800 rounded-lg overflow-hidden bg-zinc-900/20">
                                        <button onClick={() => toggleHint(hint.id, hint.type)} className="w-full flex items-center justify-between p-3 text-left hover:bg-zinc-800/50 transition-colors">
                                            <div className="flex items-center gap-2">
                                                {hint.type === 'concept' && <div className="text-[10px] bg-blue-900/30 text-blue-400 px-2 py-0.5 rounded border border-blue-500/20 uppercase tracking-wide">Concept</div>}
                                                {hint.type === 'snippet' && <div className="text-[10px] bg-amber-900/30 text-amber-400 px-2 py-0.5 rounded border border-amber-500/20 uppercase tracking-wide">Snippet</div>}
                                                {hint.type === 'solution' && <div className="text-[10px] bg-red-900/30 text-red-400 px-2 py-0.5 rounded border border-red-500/20 uppercase tracking-wide">Solution</div>}
                                                <span className="text-xs text-zinc-400 font-mono">{unlockedHints[hint.id] ? "Access Granted" : "Encrypted Data"}</span>
                                            </div>
                                            <div className="text-zinc-600">{unlockedHints[hint.id] ? <ChevronUp className="w-4 h-4" /> : <div className="flex items-center gap-1 text-[10px] uppercase font-bold text-zinc-600"><Lock className="w-3 h-3" /> Unlock</div>}</div>
                                        </button>
                                        {unlockedHints[hint.id] && (
                                            <div className="p-3 border-t border-zinc-800/50 bg-black/20 animate-in slide-in-from-top-2">
                                                <div className="prose prose-invert prose-sm max-w-none"><ReactMarkdown>{hint.text}</ReactMarkdown></div>
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        );
                    }
                    return <div className="text-zinc-500 italic text-xs text-center py-8">No hints available for this mission.</div>;
                })()}


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

                {/* TUTORIAL TAB (Phase 9.1) */}
                {activeTab === 'tutorial' && customPanels?.tutorial && (
                    <div className="animate-in fade-in slide-in-from-bottom-2 duration-300">
                        {customPanels.tutorial}
                    </div>
                )}
                {/* DATABASE TAB (Phase 9.2) */}
                {activeTab === 'database' && customPanels?.database && (
                    <div className="animate-in fade-in slide-in-from-bottom-2 duration-300 h-full">
                        {customPanels.database}
                    </div>
                )}
            </div>
        </div>
    );
}
