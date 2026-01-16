import React, { useState, useEffect, useMemo, useRef } from 'react';
import { QuestSummary } from '@/lib/questsApi';
import { QuestEditor, QuestEditorRef } from './QuestEditor';
import { QuestDrawer } from './QuestDrawer';
import { QuestSuccessOverlay } from './QuestSuccessOverlay';
import { Play, RotateCcw, CheckCircle2, Terminal as TerminalIcon, Copy, Info, AlertTriangle, Check, FileCode } from 'lucide-react';

interface QuestIDEProps {
    quest: QuestSummary;
    onBack?: () => void;
}

type ConsoleEntry = {
    type: 'info' | 'success' | 'error' | 'output';
    content: string;
    timestamp: number;
};

export function QuestIDE({ quest, onBack }: QuestIDEProps) {
    const editorRef = useRef<QuestEditorRef>(null);
    const [code, setCode] = useState(quest.starter_code || "# Start coding here...\n");
    const [output, setOutput] = useState<ConsoleEntry[]>([]);
    const [isRunning, setIsRunning] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [showSuccess, setShowSuccess] = useState(false);

    // Derived Objectives State
    const objectivesState = useMemo(() => {
        const state: Record<string, boolean> = {};
        if (quest.objectives) {
            quest.objectives.forEach(obj => {
                let passed = false;
                if (obj.validator.kind === 'contains') {
                    passed = code.includes(obj.validator.value);
                } else if (obj.validator.kind === 'regex') {
                    try {
                        passed = new RegExp(obj.validator.value, 'm').test(code);
                    } catch (e) { passed = false; }
                }
                state[obj.id] = passed;
            });
        }
        return state;
    }, [code, quest.objectives]);

    const passedCount = Object.values(objectivesState).filter(Boolean).length;
    const totalCount = quest.objectives?.length || 0;
    const allPassed = totalCount > 0 && passedCount === totalCount;

    const addLog = (content: string, type: ConsoleEntry['type'] = 'output') => {
        setOutput(prev => [...prev, { type, content, timestamp: Date.now() }]);
    };

    const handleObjectiveClick = (objId: string) => {
        const obj = quest.objectives?.find(o => o.id === objId);
        if (!obj) return;

        // Naive line finder
        const lines = code.split('\n');
        const lineIdx = lines.findIndex(l =>
            obj.validator.kind === 'contains' ? l.includes(obj.validator.value)
                : new RegExp(obj.validator.value).test(l)
        );

        if (lineIdx !== -1 && editorRef.current) {
            editorRef.current.jumpToLine(lineIdx + 1);
        }
    };

    const handleRun = async () => {
        setIsRunning(true);
        setOutput([]);
        addLog('Compiling...', 'info');

        try {
            // Import dynamically to avoid cycle if any, though questsApi is safe
            const { runQuest } = await import('@/lib/questsApi');
            const result = await runQuest(quest.slug, code, "python");

            // Show Output
            if (result.stdout) addLog(result.stdout, 'output');
            if (result.stderr) addLog(result.stderr, 'error');

            if (result.passed) {
                addLog('SUCCESS All objectives verified.', 'success');
                addLog('Ready for submission.', 'info');
            } else {
                addLog('Execution completed with warnings.', 'error');
                result.objective_results.forEach(obj => {
                    if (!obj.ok) addLog(`[FAIL] ${obj.id}: ${obj.detail || 'Requirement not met'}`, 'error');
                });
            }
        } catch (e: any) {
            addLog(`Runtime Error: ${e.message}`, 'error');
        } finally {
            setIsRunning(false);
        }
    };

    const handleSubmit = async () => {
        if (!allPassed) return;

        try {
            const { submitQuestSolution } = await import('@/lib/questsApi');
            const result = await submitQuestSolution(quest.slug, code, "python");

            if (result.passed) {
                // 1. Success Overlay
                setShowSuccess(true);
            } else {
                addLog('Submission rejected by server.', 'error');
            }
        } catch (e: any) {
            addLog(`Submission Error: ${e.message}`, 'error');
        }
    };

    // Auto-save
    useEffect(() => {
        setIsSaving(true);
        const key = `evalforge:code:${quest.id}`;
        localStorage.setItem(key, code);
        const t = setTimeout(() => setIsSaving(false), 800);
        return () => clearTimeout(t);
    }, [code, quest.id]);

    // Restore
    useEffect(() => {
        const key = `evalforge:code:${quest.id}`;
        const saved = localStorage.getItem(key);
        if (saved) {
            setCode(saved);
        }
    }, [quest.id]);

    return (
        <div className="h-full flex flex-col bg-black/40 rounded-xl border border-zinc-800 overflow-hidden shadow-inner relative">

            {showSuccess && (
                <QuestSuccessOverlay
                    quest={quest}
                    onClose={() => setShowSuccess(false)}
                    onNext={() => {
                        setShowSuccess(false);
                        onBack?.();
                    }}
                />
            )}

            {/* Header */}
            <div className="h-14 border-b border-zinc-800 bg-zinc-900/80 backdrop-blur-md flex items-center justify-between px-4 shrink-0">
                <div className="flex items-center gap-4">
                    <button onClick={onBack} className="text-zinc-500 hover:text-zinc-300 transition-colors">
                        ←
                    </button>
                    <div>
                        <div className="text-xs font-bold text-zinc-500 uppercase tracking-widest leading-none mb-1">Mission Control</div>
                        <div className="flex items-center gap-3">
                            <span className="text-sm font-bold text-cyan-100">{quest.title}</span>
                            <div className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wide border ${allPassed ? 'bg-emerald-950/40 text-emerald-400 border-emerald-500/30' : 'bg-zinc-900 text-zinc-500 border-zinc-700'}`}>
                                {passedCount}/{totalCount} Objectives
                            </div>
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-2">
                    <button
                        onClick={() => setCode(quest.starter_code || "")}
                        className="p-2 text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800 rounded-lg transition-all"
                        title="Reset Code"
                    >
                        <RotateCcw className="w-4 h-4" />
                    </button>

                    <div className="h-6 w-px bg-zinc-800 mx-1" />

                    <button
                        onClick={handleRun}
                        disabled={isRunning}
                        className={`
                            flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-widest transition-all
                            ${isRunning
                                ? 'bg-zinc-800 text-zinc-500'
                                : 'bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700'
                            }
                        `}
                    >
                        <Play className="w-3 h-3 fill-current" />
                        Run
                    </button>

                    <button
                        onClick={handleSubmit}
                        disabled={!allPassed || isRunning}
                        className={`
                            flex items-center gap-2 px-6 py-2 rounded-lg text-xs font-bold uppercase tracking-widest transition-all shadow-lg
                            ${allPassed
                                ? 'bg-emerald-500 hover:bg-emerald-400 text-black shadow-emerald-900/20'
                                : 'bg-zinc-900 text-zinc-600 border border-zinc-800 cursor-not-allowed'
                            }
                        `}
                    >
                        {allPassed ? <CheckCircle2 className="w-4 h-4" /> : <TerminalIcon className="w-4 h-4" />}
                        Submit
                    </button>
                </div>
            </div>

            {/* Split Pane */}
            <div className="flex-1 grid grid-cols-1 lg:grid-cols-[320px_1fr] min-h-0">
                <div className="hidden lg:block border-r border-zinc-800 bg-zinc-950/30">
                    <QuestDrawer
                        quest={quest}
                        objectivesState={objectivesState}
                        onObjectiveClick={handleObjectiveClick}
                    />
                </div>

                <div className="flex flex-col min-h-0 bg-zinc-950 relative">
                    <div className="flex-1 min-h-0">
                        <QuestEditor
                            ref={editorRef}
                            value={code}
                            onChange={setCode}
                            language="python"
                            isSaving={isSaving}
                        />
                    </div>

                    {/* Rich Console */}
                    <div className="h-48 border-t border-zinc-800 bg-[#09090b] flex flex-col shrink-0 font-mono">
                        <div className="px-3 py-1.5 border-b border-zinc-800/50 flex justify-between items-center bg-black/20">
                            <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-500 flex items-center gap-2">
                                <TerminalIcon className="w-3 h-3" /> Terminal Output
                            </span>
                            <div className="flex gap-2">
                                <button title="Copy Output" onClick={() => navigator.clipboard.writeText(output.map(o => o.content).join('\n'))} className="text-zinc-600 hover:text-zinc-400 p-1 hover:bg-zinc-800 rounded"><Copy className="w-3 h-3" /></button>
                                <button onClick={() => setOutput([])} className="text-zinc-600 hover:text-zinc-400 text-[10px] uppercase p-1 hover:bg-zinc-800 rounded">Clear</button>
                            </div>
                        </div>
                        <div className="flex-1 overflow-auto p-3 space-y-1">
                            {!output.length && <div className="text-zinc-700 italic text-xs">// Ready to run...</div>}
                            {output.map((entry, i) => (
                                <div key={i} className="flex gap-2 text-xs items-start animate-in fade-in slide-in-from-left-1 duration-200">
                                    <span className="text-zinc-700 shrink-0 select-none">
                                        {new Date(entry.timestamp).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                                    </span>
                                    <div className="flex-1 break-all whitespace-pre-wrap">
                                        {entry.type === 'info' && <span className="text-cyan-500 font-bold mr-2">INFO</span>}
                                        {entry.type === 'success' && <span className="text-emerald-500 font-bold mr-2">SUCCESS</span>}
                                        {entry.type === 'error' && <span className="text-amber-500 font-bold mr-2">WARN</span>}
                                        <span className={
                                            entry.type === 'success' ? 'text-emerald-200' :
                                                entry.type === 'error' ? 'text-amber-200' :
                                                    entry.type === 'info' ? 'text-cyan-200' :
                                                        'text-zinc-300'
                                        }>{entry.content}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
