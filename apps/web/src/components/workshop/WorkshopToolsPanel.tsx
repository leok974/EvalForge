import React from 'react';
import { PanelId, WORKSHOP_PANELS } from '../../features/workshop/workshopPanels';
import { cn } from '../../lib/utils';
import { Terminal, BookOpen, Bug, MessageSquare } from 'lucide-react';

interface WorkshopToolsPanelProps {
    activePanel: PanelId;
    onPanelChange: (panel: PanelId) => void;

    // Context Content
    resultsContent?: React.ReactNode;
    codexContent?: React.ReactNode;

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
    codexContent,
    hasSkill
}) => {

    // Helper to check lock state
    const isLocked = (id: PanelId) => {
        const def = WORKSHOP_PANELS[id];
        return !def.isEnabled({ hasSkill });
    };

    return (
        <div className="flex flex-col h-full bg-slate-950/50 rounded-xl border border-white/5 overflow-hidden">
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
                        <div className="p-3 rounded bg-amber-950/20 border border-amber-900/30 text-amber-200/80 text-xs">
                            <h4 className="font-bold mb-1 flex items-center gap-2">
                                <MessageSquare className="w-3 h-3" />
                                Analysis
                            </h4>
                            <p>This panel will analyze your current quest state and provide hints.</p>
                            {/* TODO: Hook up to /api/assist/explain */}
                            <button className="mt-2 w-full py-1 bg-amber-900/40 hover:bg-amber-800/40 border border-amber-700/50 rounded text-[10px] uppercase tracking-wider font-bold transition-colors">
                                Analyze Code
                            </button>
                        </div>
                    </div>
                )}

                {/* 3. Debug */}
                {activePanel === 'debug' && (
                    <div className="space-y-4 animate-in fade-in zoom-in-95 duration-200">
                        <div className="p-3 rounded bg-rose-950/20 border border-rose-900/30 text-rose-200/80 text-xs">
                            <h4 className="font-bold mb-1 flex items-center gap-2">
                                <Bug className="w-3 h-3" />
                                Debugger
                            </h4>
                            <p>This panel will inspect failures and propose fixes.</p>
                            {/* TODO: Hook up to /api/assist/debug */}
                            <button className="mt-2 w-full py-1 bg-rose-900/40 hover:bg-rose-800/40 border border-rose-700/50 rounded text-[10px] uppercase tracking-wider font-bold transition-colors">
                                Inspect Failures
                            </button>
                        </div>
                    </div>
                )}

                {/* 4. Codex */}
                {activePanel === 'codex' && (
                    <div className="h-full animate-in fade-in zoom-in-95 duration-200">
                        {codexContent || <div className="text-zinc-500 text-xs italic">Codex unavailable.</div>}
                    </div>
                )}
            </div>
        </div>
    );
};
