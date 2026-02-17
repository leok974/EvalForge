import React from 'react';
import { useQuestStore } from '../../store/questStore';
import { CodexPanel } from '../../features/codex/CodexPanel';
import { PanelId, WORKSHOP_PANELS } from '../../features/workshop/workshopPanels';
import { cn } from '../../lib/utils';
import { Terminal, BookOpen, Bug, MessageSquare, Play } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { useCoach } from '../../hooks/useCoach';

interface WorkshopToolsPanelProps {
    activePanel: PanelId;
    onPanelChange: (panel: PanelId) => void;

    // Context Content
    resultsContent?: React.ReactNode;

    // Codex Props
    questSlug?: string;
    initialCodexTerm?: string;

    // Skills
    hasSkill: (skill: string) => boolean;
}

const ICONS: Record<PanelId, React.ReactNode> = {
    judge: <Terminal className="w-3 h-3" />,
    explain: <MessageSquare className="w-3 h-3" />,
    debug: <Bug className="w-3 h-3" />,
    codex: <BookOpen className="w-3 h-3" />
};

export const WorkshopToolsPanel: React.FC<WorkshopToolsPanelProps> = ({
    activePanel,
    onPanelChange,
    resultsContent,
    questSlug,
    initialCodexTerm,
    hasSkill
}) => {
    // 1. Store Access
    const { lastRunResult } = useQuestStore();

    // 2. Coach Hooks
    const explainCoach = useCoach('explain');
    const debugCoach = useCoach('debug');

    // Helpers
    const isLocked = (id: PanelId) => {
        const def = WORKSHOP_PANELS[id];
        return !def.isEnabled({ hasSkill });
    };

    return (
        <div className="flex flex-col h-full bg-slate-950/50 rounded-xl border border-white/5 overflow-hidden" data-testid="workshop-tools-panel">
            {/* Tabs Header */}
            <div className="flex border-b border-white/5 bg-black/20">
                {Object.values(WORKSHOP_PANELS).map((panel) => {
                    const locked = isLocked(panel.id);
                    const isActive = activePanel === panel.id;

                    return (
                        <button
                            key={panel.id}
                            onClick={() => !locked && onPanelChange(panel.id)}
                            disabled={locked}
                            className={cn(
                                "flex-1 px-3 py-2 text-[10px] uppercase font-bold tracking-wider transition-colors flex items-center justify-center gap-2 border-b-2",
                                isActive
                                    ? "text-workshop-cyan border-workshop-cyan bg-workshop-cyan/5"
                                    : "text-workshop-subtle border-transparent hover:text-workshop-text hover:bg-white/5",
                                locked && "opacity-40 cursor-not-allowed"
                            )}
                            title={locked ? panel.disabledReason?.({ hasSkill }) : panel.description}
                        >
                            {ICONS[panel.id]}
                            <span className="hidden xl:inline">{panel.label}</span>
                            {locked && <span className="text-[8px]">🔒</span>}
                        </button>
                    );
                })}
            </div>

            {/* Panel Content Area */}
            <div className="flex-1 overflow-y-auto p-4 relative">
                {/* 1. Results (Judge) */}
                {activePanel === 'judge' && (
                    <div className="space-y-4 animate-in fade-in zoom-in-95 duration-200">
                        {resultsContent || <div className="text-zinc-500 text-xs italic">No results available. Submit your code to see the verdict.</div>}
                    </div>
                )}

                {/* 2. Explain */}
                {activePanel === 'explain' && (
                    <div className="space-y-4 animate-in fade-in zoom-in-95 duration-200">
                        {explainCoach.loading && <div className="text-xs text-workshop-cyan animate-pulse">Analyzing...</div>}
                        {explainCoach.error && <div className="text-xs text-rose-400 border border-rose-900/50 p-2 rounded bg-rose-950/30">Error: {explainCoach.error}</div>}

                        {!explainCoach.data ? (
                            <div className="p-3 rounded bg-amber-950/20 border border-amber-900/30 text-amber-200/80 text-xs">
                                <h4 className="font-bold mb-1 flex items-center gap-2">
                                    <MessageSquare className="w-3 h-3" />
                                    Explain
                                </h4>
                                <p className="mb-3">Get a conceptual explanation of your current work.</p>
                                <button
                                    onClick={explainCoach.invoke}
                                    disabled={explainCoach.loading}
                                    className="w-full py-1.5 bg-amber-900/40 hover:bg-amber-800/40 disabled:opacity-50 disabled:cursor-not-allowed border border-amber-700/50 rounded text-[10px] uppercase tracking-wider font-bold transition-colors"
                                >
                                    {lastRunResult ? "Explain Current State" : "Run Code First"}
                                </button>
                            </div>
                        ) : (
                            <div className="space-y-3">
                                {/* Summary Markdown */}
                                <div className="text-sm text-slate-300 prose prose-invert prose-p:leading-relaxed prose-pre:bg-black/50 prose-pre:border prose-pre:border-white/10">
                                    <ReactMarkdown>{explainCoach.data.summary_md}</ReactMarkdown>
                                </div>

                                {/* Hypotheses */}
                                {explainCoach.data.hypotheses.length > 0 && (
                                    <div className="text-xs text-slate-300 bg-black/20 p-2 rounded border border-white/5">
                                        <span className="text-amber-500 font-bold block mb-2">Key Concepts:</span>
                                        <ul className="list-disc pl-4 space-y-2">
                                            {explainCoach.data.hypotheses.map((h, i) => (
                                                <li key={i}>
                                                    <strong className="text-amber-200">{h.title}</strong>
                                                    <br />
                                                    <span className="opacity-80">{h.evidence.join(' ')}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                {/* Next Steps */}
                                {explainCoach.data.next_steps.length > 0 && (
                                    <div className="text-xs">
                                        <span className="text-workshop-subtle font-bold uppercase tracking-wider mb-2 block">Recommended Steps</span>
                                        <ul className="space-y-2">
                                            {explainCoach.data.next_steps.map((s, i) => (
                                                <li key={i} className="flex gap-2 items-start text-slate-300 bg-white/5 p-2 rounded border border-white/5">
                                                    <Play className="w-3 h-3 mt-0.5 text-workshop-cyan shrink-0" />
                                                    <div>
                                                        <strong className="block text-cyan-200">{s.label}</strong>
                                                    </div>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                                <button onClick={explainCoach.clear} className="text-[10px] text-zinc-500 hover:text-zinc-300 underline">Clear</button>
                            </div>
                        )}
                    </div>
                )}

                {/* 3. Debug */}
                {activePanel === 'debug' && (
                    <div className="space-y-4 animate-in fade-in zoom-in-95 duration-200">
                        {debugCoach.loading && <div className="text-xs text-workshop-cyan animate-pulse">Debugging...</div>}
                        {debugCoach.error && <div className="text-xs text-rose-400 border border-rose-900/50 p-2 rounded bg-rose-950/30">Error: {debugCoach.error}</div>}

                        {!debugCoach.data ? (
                            <div className="p-3 rounded bg-rose-950/20 border border-rose-900/30 text-rose-200/80 text-xs">
                                <h4 className="font-bold mb-1 flex items-center gap-2">
                                    <Bug className="w-3 h-3" />
                                    Debug
                                </h4>
                                <p className="mb-3">Analyze failures and get a repair plan.</p>
                                <button
                                    onClick={debugCoach.invoke}
                                    disabled={debugCoach.loading}
                                    className="w-full py-1.5 bg-rose-900/40 hover:bg-rose-800/40 disabled:opacity-50 disabled:cursor-not-allowed border border-rose-700/50 rounded text-[10px] uppercase tracking-wider font-bold transition-colors"
                                >
                                    {lastRunResult ? "Debug Last Failure" : "Run Code First"}
                                </button>
                            </div>
                        ) : (
                            <div className="space-y-3">
                                {/* Summary */}
                                <div className="text-sm text-slate-300 prose prose-invert prose-p:leading-relaxed">
                                    <ReactMarkdown>{debugCoach.data.summary_md}</ReactMarkdown>
                                </div>

                                {/* Root Causes */}
                                {debugCoach.data.hypotheses.length > 0 && (
                                    <div className="text-xs text-slate-300 bg-black/20 p-2 rounded border border-rose-900/20">
                                        <span className="text-rose-400 font-bold block mb-2">Root Causes:</span>
                                        <ul className="list-disc pl-4 space-y-2">
                                            {debugCoach.data.hypotheses.map((h, i) => (
                                                <li key={i}>
                                                    <strong className="text-rose-200">{h.title}</strong>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                {/* Fix Plan */}
                                {debugCoach.data.next_steps.length > 0 && (
                                    <div className="text-xs">
                                        <span className="text-workshop-subtle font-bold uppercase tracking-wider mb-2 block">Fix Plan</span>
                                        <ol className="list-decimal pl-4 space-y-2 text-slate-300">
                                            {debugCoach.data.next_steps.map((s, i) => (
                                                <li key={i} className="pl-1">
                                                    <span className="font-bold text-slate-200">{s.label}</span>
                                                </li>
                                            ))}
                                        </ol>
                                    </div>
                                )}

                                {/* Patch UI (Only if allowed by data, backend strips it for students) */}
                                {debugCoach.data.patch && (
                                    <div className="text-xs border border-white/10 rounded overflow-hidden">
                                        <div className="bg-white/5 px-2 py-1 font-mono text-[10px] border-b border-white/10">SUGGESTED PATCH</div>
                                        <pre className="p-2 bg-black/50 overflow-x-auto text-[10px] font-mono text-emerald-300">
                                            {debugCoach.data.patch.unified_diff}
                                        </pre>
                                    </div>
                                )}

                                <button onClick={debugCoach.clear} className="text-[10px] text-zinc-500 hover:text-zinc-300 underline">Clear</button>
                            </div>
                        )}
                    </div>
                )}

                {/* 4. Codex */}
                {activePanel === 'codex' && (
                    <div className="h-full animate-in fade-in zoom-in-95 duration-200 -m-4">
                        <CodexPanel
                            questSlug={questSlug}
                            initialTerm={initialCodexTerm}
                        />
                    </div>
                )}
            </div>
        </div>
    );
};
