import React from 'react';
import { useQuestStore } from '../../store/questStore';
import { CodexPanel } from '../../features/codex/CodexPanel';
import { PanelId, WORKSHOP_PANELS } from '../../features/workshop/workshopPanels';
import { cn } from '../../lib/utils';
import { Terminal, BookOpen, Bug, MessageSquare } from 'lucide-react';

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
    // 1. Store Access (Last Run Context)
    const { lastRunResult } = useQuestStore();

    // 2. Local State for Tools
    const [explainData, setExplainData] = React.useState<any>(null);
    const [debugData, setDebugData] = React.useState<any>(null);
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState<string | null>(null);

    // Helpers
    const isLocked = (id: PanelId) => {
        const def = WORKSHOP_PANELS[id];
        return !def.isEnabled({ hasSkill });
    };

    const handleExplain = async () => {
        if (!questSlug) return;
        setLoading(true);
        setError(null);
        try {
            const payload = {
                quest_slug: questSlug,
                stdout: lastRunResult?.stdout || undefined,
                stderr: lastRunResult?.stderr || undefined,
                failing_tests: lastRunResult?.test_summary?.failures?.map((f: any) => f.name) || undefined,
                // user_skill_level? could pull from profile store
            };
            const { explainQuest } = await import('@/lib/toolsApi');
            const data = await explainQuest(payload);
            setExplainData(data);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleDebug = async () => {
        if (!questSlug) return;
        setLoading(true);
        setError(null);
        try {
            const payload = {
                quest_slug: questSlug,
                stdout: lastRunResult?.stdout || undefined,
                stderr: lastRunResult?.stderr || undefined,
                failing_tests: lastRunResult?.test_summary?.failures?.map((f: any) => f.name) || undefined,
            };
            const { debugQuest } = await import('@/lib/toolsApi');
            const data = await debugQuest(payload);
            setDebugData(data);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
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
                        {loading && <div className="text-xs text-workshop-cyan animate-pulse">Running Analysis...</div>}
                        {error && <div className="text-xs text-rose-400 border border-rose-900/50 p-2 rounded bg-rose-950/30">Error: {error}</div>}

                        {!explainData ? (
                            <div className="p-3 rounded bg-amber-950/20 border border-amber-900/30 text-amber-200/80 text-xs">
                                <h4 className="font-bold mb-1 flex items-center gap-2">
                                    <MessageSquare className="w-3 h-3" />
                                    Analysis
                                </h4>
                                <p className="mb-3">Run your code, then ask for an explanation of the results.</p>
                                <button
                                    onClick={handleExplain}
                                    disabled={!lastRunResult || loading}
                                    className="w-full py-1.5 bg-amber-900/40 hover:bg-amber-800/40 disabled:opacity-50 disabled:cursor-not-allowed border border-amber-700/50 rounded text-[10px] uppercase tracking-wider font-bold transition-colors"
                                >
                                    {lastRunResult ? "Analyze Last Run" : "Run Code First"}
                                </button>
                            </div>
                        ) : (
                            <div className="space-y-3">
                                <div className="text-sm font-bold text-amber-300">{explainData.summary}</div>
                                <div className="text-xs text-slate-300 bg-black/20 p-2 rounded border border-white/5">
                                    <span className="text-amber-500 font-bold block mb-1">Observation:</span>
                                    {explainData.what_happened}
                                </div>
                                <div className="text-xs text-slate-300 bg-black/20 p-2 rounded border border-white/5">
                                    <span className="text-amber-500 font-bold block mb-1">Reason:</span>
                                    {explainData.why_it_failed}
                                </div>
                                {explainData.next_steps?.length > 0 && (
                                    <div className="text-xs">
                                        <span className="text-workshop-subtle font-bold uppercase tracking-wider mb-1 block">Recommended Steps</span>
                                        <ul className="list-disc pl-4 space-y-1 text-slate-300">
                                            {explainData.next_steps.map((s: string, i: number) => <li key={i}>{s}</li>)}
                                        </ul>
                                    </div>
                                )}
                                <button onClick={() => setExplainData(null)} className="text-[10px] text-zinc-500 hover:text-zinc-300 underline">Clear</button>
                            </div>
                        )}
                    </div>
                )}

                {/* 3. Debug */}
                {activePanel === 'debug' && (
                    <div className="space-y-4 animate-in fade-in zoom-in-95 duration-200">
                        {loading && <div className="text-xs text-workshop-cyan animate-pulse">Running Debugger...</div>}
                        {error && <div className="text-xs text-rose-400 border border-rose-900/50 p-2 rounded bg-rose-950/30">Error: {error}</div>}

                        {!debugData ? (
                            <div className="p-3 rounded bg-rose-950/20 border border-rose-900/30 text-rose-200/80 text-xs">
                                <h4 className="font-bold mb-1 flex items-center gap-2">
                                    <Bug className="w-3 h-3" />
                                    Debugger
                                </h4>
                                <p className="mb-3">Analyze failures and get a repair plan.</p>
                                <button
                                    onClick={handleDebug}
                                    disabled={!lastRunResult || loading}
                                    className="w-full py-1.5 bg-rose-900/40 hover:bg-rose-800/40 disabled:opacity-50 disabled:cursor-not-allowed border border-rose-700/50 rounded text-[10px] uppercase tracking-wider font-bold transition-colors"
                                >
                                    {lastRunResult ? "Debug Last Failure" : "Run Code First"}
                                </button>
                            </div>
                        ) : (
                            <div className="space-y-3">
                                <div className="text-sm font-bold text-rose-300">{debugData.summary}</div>
                                {debugData.likely_root_causes?.length > 0 && (
                                    <div className="text-xs text-slate-300 bg-black/20 p-2 rounded border border-white/5">
                                        <span className="text-rose-500 font-bold block mb-1">Root Causes:</span>
                                        <ul className="list-disc pl-4 space-y-1">
                                            {debugData.likely_root_causes.map((c: string, i: number) => <li key={i}>{c}</li>)}
                                        </ul>
                                    </div>
                                )}
                                {debugData.fix_plan?.length > 0 && (
                                    <div className="text-xs">
                                        <span className="text-workshop-subtle font-bold uppercase tracking-wider mb-1 block">Fix Plan</span>
                                        <ol className="list-decimal pl-4 space-y-1 text-slate-300">
                                            {debugData.fix_plan.map((s: string, i: number) => <li key={i}>{s}</li>)}
                                        </ol>
                                    </div>
                                )}
                                <button onClick={() => setDebugData(null)} className="text-[10px] text-zinc-500 hover:text-zinc-300 underline">Clear</button>
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
