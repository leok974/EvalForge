import React, { useState } from 'react';
import { Bot, Sparkles, AlertTriangle, ArrowRight } from 'lucide-react';
import { fetchCoachFeedback, CoachRequest, CoachResponse } from '@/lib/coachApi';
import { MarkdownSurface } from '@/components/markdown/MarkdownSurface';
import { QuestSummary } from '@/lib/questsApi';

interface CoachPanelProps {
    mode: 'explain' | 'debug';
    quest: QuestSummary;
    lastRunResult: any;
    attemptId?: string;
    workspaceFiles: Record<string, { content: string; editable?: boolean }>;
}

export function CoachPanel({ mode, quest, lastRunResult, attemptId, workspaceFiles }: CoachPanelProps) {
    const [loading, setLoading] = useState(false);
    const [response, setResponse] = useState<CoachResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    // Deterministic check for empty SQL
    const isConfigEmptySql = mode === 'debug' && quest.language === 'sql' && lastRunResult && (
        (lastRunResult.stdout && lastRunResult.stdout.includes('CONFIG_EMPTY_SQL')) ||
        (lastRunResult.stderr && lastRunResult.stderr.includes('CONFIG_EMPTY_SQL')) ||
        (lastRunResult.error && lastRunResult.error.includes('CONFIG_EMPTY_SQL')));

    const handleAskCoach = async () => {
        if (!lastRunResult) return;
        setLoading(true);
        setError(null);
        try {
            // Prepare workspace files
            const files = Object.entries(workspaceFiles).map(([path, f]) => ({
                path,
                content: f.content
            }));

            const payload: CoachRequest = {
                mode,
                world: quest.world_id || 'general',
                quest_slug: quest.slug,
                student_mode: true,
                runner_result: lastRunResult,
                terminal_output_text: lastRunResult.stdout || lastRunResult.stderr || '',
                workspace_files: files,
                attempt_id: attemptId
            };

            const res = await fetchCoachFeedback(payload);
            setResponse(res);
        } catch (e: any) {
            setError(e.message || "Failed to contact Coach.");
        } finally {
            setLoading(false);
        }
    };

    if (!lastRunResult) {
        return (
            <div className="flex flex-col items-center justify-center p-8 text-zinc-500 text-xs italic space-y-2 h-full">
                <Bot className="w-8 h-8 opacity-20 mb-2" />
                <p>No run data available.</p>
                <p>Submit your code first to get {mode === 'debug' ? 'debugging help' : 'an explanation'}.</p>
            </div>
        );
    }

    if (isConfigEmptySql) {
        return (
            <div className="p-4 space-y-4 font-mono text-sm max-w-3xl mx-auto">
                <div className="flex items-center gap-3 text-amber-500 mb-2">
                    <AlertTriangle className="w-5 h-5" />
                    <h3 className="font-bold uppercase tracking-widest">Entrypoint Missing</h3>
                </div>
                <div className="p-4 rounded-lg bg-amber-950/20 border border-amber-900/50 text-amber-200/80">
                    <p className="mb-2">Your <code>task.sql</code> is empty or not being read.</p>
                    <p>Edit <code>task.sql</code> and ensure it contains a <code>SELECT...</code> statement.</p>
                </div>
            </div>
        );
    }

    if (!response && !loading) {
        return (
            <div className="flex flex-col items-center justify-center p-8 space-y-4 h-full">
                <div className="p-4 rounded-full bg-indigo-500/10 mb-2">
                    <Bot className="w-12 h-12 text-indigo-400 opacity-80" />
                </div>
                <h3 className="text-zinc-200 font-mono text-sm text-center max-w-md leading-relaxed">
                    Need help {mode === 'debug' ? 'figuring out why this failed' : 'understanding these results'}?
                </h3>
                <button
                    onClick={handleAskCoach}
                    className="flex items-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-bold text-sm shadow-[0_0_20px_rgba(79,70,229,0.3)] transition-all hover:scale-105"
                >
                    <Sparkles className="w-4 h-4" />
                    Ask Coach {mode === 'debug' ? 'to Debug' : 'to Explain'}
                </button>
            </div>
        );
    }

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center p-12 space-y-4 h-full">
                <div className="w-8 h-8 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin mb-2" />
                <p className="text-indigo-300/80 font-mono text-xs animate-pulse">
                    Coach is analyzing your {mode === 'debug' ? 'code and errors' : 'approach'}...
                </p>
            </div>
        );
    }

    return (
        <div className="h-full overflow-y-auto p-4 md:p-6 lg:p-8 custom-scrollbar">
            <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-300">

                {/* Error Banner if API failed */}
                {error && (
                    <div className="p-4 bg-red-950/50 border border-red-900/50 rounded-xl text-red-200">
                        <div className="flex items-center gap-2 font-bold mb-1"><AlertTriangle className="w-4 h-4" /> Coach Error</div>
                        <div className="text-sm font-mono opacity-80">{error}</div>
                    </div>
                )}

                {response && (
                    <>
                        {/* Summary Section */}
                        <div className="prose prose-invert prose-indigo max-w-none 
                            prose-pre:bg-black/40 prose-pre:border prose-pre:border-indigo-500/20
                            prose-h3:text-indigo-300 prose-h3:font-normal prose-h3:tracking-wide">
                            <MarkdownSurface md={response.summary_md} />
                        </div>

                        {/* Hypotheses (Debug only usually) */}
                        {response.hypotheses && response.hypotheses.length > 0 && (
                            <div className="space-y-4 mt-8">
                                <h4 className="text-xs font-bold uppercase tracking-widest text-zinc-500 font-mono">Analysis</h4>
                                <div className="grid gap-4">
                                    {response.hypotheses.map((hyp, i) => (
                                        <div key={i} className="p-4 rounded-xl bg-zinc-900/50 border border-zinc-800">
                                            <h5 className="font-bold text-zinc-200 mb-2">{hyp.title}</h5>
                                            <ul className="space-y-1">
                                                {hyp.evidence.map((ev, j) => (
                                                    <li key={j} className="text-sm text-zinc-400 flex items-start gap-2">
                                                        <span className="text-indigo-500 mt-1">•</span> {ev}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Next Steps */}
                        {response.next_steps && response.next_steps.length > 0 && (
                            <div className="space-y-4 mt-8">
                                <h4 className="text-xs font-bold uppercase tracking-widest text-zinc-500 font-mono">Next Steps</h4>
                                <div className="space-y-2">
                                    {response.next_steps.map((step, i) => (
                                        <div key={i} className="flex items-start gap-4 p-4 rounded-xl bg-indigo-950/20 border border-indigo-900/30">
                                            <div className="mt-0.5"><ArrowRight className="w-4 h-4 text-indigo-400" /></div>
                                            <div className="flex-1">
                                                <div className="font-medium text-indigo-200">{step.label}</div>
                                                <div className="text-sm text-indigo-200/60 font-mono mt-1">{step.action}</div>
                                                {step.target && <div className="text-xs text-zinc-500 mt-2">Target: {step.target}</div>}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Patch (Optional) */}
                        {response.patch && response.patch.unified_diff && (
                            <div className="space-y-4 mt-8">
                                <h4 className="text-xs font-bold uppercase tracking-widest text-zinc-500 font-mono mb-2">Suggested Fix</h4>
                                <div className="text-sm">
                                    <MarkdownSurface md={`\`\`\`diff\n${response.patch.unified_diff}\n\`\`\``} />
                                </div>
                            </div>
                        )}

                    </>
                )}
            </div>
        </div>
    );
}
