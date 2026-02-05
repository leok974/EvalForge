import React, { useState, useEffect, useMemo, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { QuestSummary, QuestAttemptSummary, fetchQuestAttempts, fetchQuestAttempt, unlockHint, fetchQuest } from '@/lib/questsApi';
import { QuestEditor, QuestEditorRef } from './QuestEditor';
import { QuestDrawer } from './QuestDrawer';
import { TutorialPanel } from './TutorialPanel'; // Phase 9.1
import { CodexDrawer } from '../codex/CodexDrawer'; // Phase 9.1
import { QuestSuccessOverlay } from './QuestSuccessOverlay';
import { CoachBanner, CoachData } from './CoachBanner';
import { DebriefData } from './DebriefPanel';
import { ProblemsPanel } from './ProblemsPanel'; // Import
import { Diagnostic, QuickFix } from '@/lib/questsApi';
import { QuickFixBar } from './QuickFixBar';
import { AnimatePresence } from 'framer-motion';
import { Play, RotateCcw, CheckCircle2, Terminal as TerminalIcon, Copy, Info, AlertTriangle, Check, FileCode, History as HistoryIcon, Split, Download, X, Lock, Maximize2, Minimize2 } from 'lucide-react';
import { DiffEditor } from '@monaco-editor/react';
import { useQuestStore } from '@/store/questStore';

interface QuestIDEProps {
    quest: QuestSummary;
    onBack?: () => void;
}

type ConsoleEntry = {
    type: 'info' | 'success' | 'error' | 'output';
    content: string;
    timestamp: number;
};
export function QuestIDE({ quest: initialQuest, onBack }: QuestIDEProps) {
    const editorRef = useRef<QuestEditorRef>(null);
    const navigate = useNavigate();
    const { worldSlug } = useParams<{ worldSlug: string }>();
    const { focusMode, toggleFocusMode } = useQuestStore();

    // Phase 9.5: Hydrate full quest details (tutorial_md, key_terms, etc.)
    const [quest, setQuest] = useState<QuestSummary>(initialQuest);

    useEffect(() => {
        // Always fetch full quest details to ensure we have tutorial_md, key_terms, etc.
        console.log(`🔍 QuestIDE mounted for: ${initialQuest.slug}, initial tutorial_len=${initialQuest.tutorial_md?.length || 0}`);

        fetchQuest(initialQuest.slug)
            .then(fullQuest => {
                setQuest(fullQuest);
                console.log(`📖 Hydrated quest details for ${initialQuest.slug}: tutorial_len=${fullQuest.tutorial_md?.length || 0}`);

                // Auto-open tutorial if available
                if (fullQuest.tutorial_md) {
                    setDrawerTab('tutorial');
                }
            })
            .catch(err => console.error('Failed to hydrate quest details:', err));
    }, [initialQuest.slug]);

    // Coach & Drawer State
    const [coachData, setCoachData] = useState<CoachData | null>(null);
    const [debriefData, setDebriefData] = useState<DebriefData | undefined>(undefined);
    const [diagnostics, setDiagnostics] = useState<Diagnostic[]>([]);
    const [quickFixes, setQuickFixes] = useState<QuickFix[]>([]);
    const [drawerTab, setDrawerTab] = useState<'briefing' | 'objectives' | 'lore' | 'hints' | 'history' | 'tutorial' | undefined>(undefined);

    // Codex State (Phase 9.1)
    const [codexOpen, setCodexOpen] = useState(false);
    const [codexRef, setCodexRef] = useState<string | null>(null);

    const handleOpenCodex = (ref: string) => {
        console.log('📖 OPENING CODEX:', ref);
        setCodexRef(ref);
        setCodexOpen(true);
    };

    // Default Tab Logic including Tutorial
    useEffect(() => {
        if (!drawerTab) {
            // Priority: Tutorial (if exists) -> Briefing
            if (quest.tutorial_md) {
                // Check if user has seen tutorial? (Optional MVP enhancement)
                // For now, always default to tutorial if present
                setDrawerTab('tutorial');
            } else {
                setDrawerTab('briefing'); // Default to briefing if no tutorial
            }
        }
    }, [quest.id, quest.tutorial_md]); // Run when quest changes

    // Deep Link Handling (Phase 9.4)
    useEffect(() => {
        const params = new URLSearchParams(window.location.search);

        // ?tutorial=1
        if (params.get('tutorial') === '1' && quest.tutorial_md) {
            setDrawerTab('tutorial');
        }

        // ?codex=...
        const codexLink = params.get('codex');
        if (codexLink) {
            setCodexRef(codexLink);
            setCodexOpen(true);
        }
    }, [quest.id]);

    // Sync state to URL (Deep Linking Phase 9.4)
    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        let changed = false;

        // Sync Codex
        if (codexOpen && codexRef) {
            if (params.get('codex') !== codexRef) {
                params.set('codex', codexRef);
                changed = true;
            }
        } else {
            if (params.has('codex')) {
                params.delete('codex');
                changed = true;
            }
        }

        // Sync Tutorial
        if (drawerTab === 'tutorial') {
            if (params.get('tutorial') !== '1') {
                params.set('tutorial', '1');
                changed = true;
            }
        } else {
            if (params.has('tutorial')) {
                params.delete('tutorial');
                changed = true;
            }
        }

        if (changed) {
            const newUrl = `${window.location.pathname}?${params.toString()}`;
            window.history.replaceState(null, '', newUrl);
        }
    }, [codexOpen, codexRef, drawerTab]);

    // State
    // Workspace State
    const [files, setFiles] = useState<Record<string, { content: string; editable: boolean }>>({});
    const [baseFiles, setBaseFiles] = useState<Record<string, string>>({});
    const [activePath, setActivePath] = useState<string>("");

    // Legacy support: sync single file to workspace
    useEffect(() => {
        if (quest.workspace) {
            const initial: Record<string, { content: string; editable: boolean }> = {};
            const initialBase: Record<string, string> = {};
            quest.workspace.files.forEach(f => {
                initial[f.path] = { content: f.content, editable: f.editable ?? true };
                if (f.editable !== false) initialBase[f.path] = f.content;
            });
            setFiles(initial);
            setBaseFiles(initialBase);
            setActivePath(quest.workspace.entrypoint);
        } else {
            // Single File Mode
            const ext = quest.language || 'python'; // Use quest language logic in getSnapshot too
            let name = 'main.py';
            if (quest.language === 'typescript') name = 'main.ts';
            if (quest.language === 'javascript') name = 'main.js';
            if (quest.language === 'css') name = 'style.css';
            if (quest.language === 'html') name = 'index.html';
            // Fallback for python or unknown

            const content = quest.starter_code || "# Start coding here...\n";
            setFiles({ [name]: { content, editable: true } });
            setBaseFiles({ [name]: content });
            setActivePath(name);
        }
    }, [quest]);

    const [output, setOutput] = useState<ConsoleEntry[]>([]);
    const [isRunning, setIsRunning] = useState(false);
    const [autosaveStatus, setAutosaveStatus] = useState<'saved' | 'saving' | 'unsaved'>('saved');
    const [showSuccess, setShowSuccess] = useState(false);

    // Replay State
    const [replay, setReplay] = useState<{ attemptId: string; artifact: any } | null>(null);
    const isReplay = !!replay;
    const [showDiff, setShowDiff] = useState(false);
    const [diffFile, setDiffFile] = useState<string>("");

    // Computed Code/Output
    // If Replay, show replay code (snapshot). If live, show files[activePath]
    // Replay artifacts need to support multi-file too. 
    // For now assuming replay.artifact.code is single file text? 
    // Phase 6: QuestAttempt needs workspace_snapshot_json.

    const displayCode = useMemo(() => {
        if (isReplay) {
            // TODO: Handle multi-file replay if available
            // For now, if replay has workspace_snapshot, use it.
            // Fallback to .code for legacy
            return replay?.artifact.code || ""; // This is wrong for multi-file replay, fix later
        }
        return files[activePath]?.content || "";
    }, [isReplay, replay, files, activePath]);

    const isReadOnly = isReplay || (files[activePath] && !files[activePath].editable);

    // History State
    const [attempts, setAttempts] = useState<QuestAttemptSummary[]>([]);

    // Load attempts on mount
    useEffect(() => {
        fetchQuestAttempts(quest.slug).then(setAttempts).catch(console.error);
    }, [quest.slug]);

    const handleReplay = async (attemptId: string) => {
        try {
            const detail = await fetchQuestAttempt(quest.slug, attemptId);
            setReplay({ attemptId, artifact: detail });

            // Set console to replay output
            setOutput([
                { type: 'info', content: `Playback: Run #${detail.run_number || '?'}`, timestamp: Date.now() },
                { type: 'output', content: detail.stdout || "", timestamp: Date.now() },
                { type: detail.passed ? 'success' : 'error', content: detail.passed ? "Attempt Passed" : "Attempt Failed", timestamp: Date.now() }
            ]);

            // Set Debrief from replay if available
            // detail type needs to support debrief_json (it's in API but might need typing update)
            // Assuming detail object has it.
            if ((detail as any).debrief_json) {
                setDebriefData((detail as any).debrief_json);
                if (detail.passed) setShowSuccess(true);
            }
            if ((detail as any).diagnostics_json) {
                setDiagnostics((detail as any).diagnostics_json);
            } else {
                setDiagnostics([]);
            }
            if ((detail as any).quick_fixes_json) {
                setQuickFixes((detail as any).quick_fixes_json);
            } else {
                setQuickFixes([]);
            }



            // ... (rest of logic like handleCoachAction)

            // ... handleRun logic ...
            // NOTE: Need to replace implementation of handleRun and handleSubmit to set DebriefData

            // (Code omitted for brevity, assuming standard structure)

            const replayOutput: ConsoleEntry[] = (detail.stdout || "").split('\n').filter(Boolean).map((l: string) => ({ type: 'output', content: l, timestamp: Date.parse(detail.created_at) }));
            if (detail.stderr) replayOutput.push({ type: 'error', content: detail.stderr, timestamp: Date.parse(detail.created_at) });

            // Allow user to see "what happened"
            setOutput(replayOutput);
        } catch (e) {
            console.error("Failed to replay", e);
        }
    };

    const exitReplay = () => {
        setReplay(null);
        setShowDiff(false);
        setOutput([]); // or restore previous output? For now clear to avoid confusion
    };

    const handleExportReport = async () => {
        if (!replay) return;
        try {
            const res = await fetch(`/api/quests/${quest.slug}/attempts/${replay.attemptId}/report?format=md`, {
                headers: { 'Authorization': 'Bearer ' + 'dev-token' } // TODO: use real auth hook if needed or cookie
            });
            if (res.ok) {
                const data = await res.json();
                const blob = new Blob([data.report], { type: 'text/markdown' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `run_report_${replay.artifact.run_number}.md`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }
        } catch (e) {
            console.error(e);
            addLog("Failed to export report", "error");
        }
    };

    // Compute Diff Content
    const getSnapshotContent = (path: string) => {
        if (!replay) return "";
        // Try workspace snapshot first (Phase 6)
        const snapshot = replay.artifact.workspace_snapshot_json as { path: string, content: string }[];
        if (snapshot) {
            const f = snapshot.find(f => f.path === path);
            return f ? f.content : ""; // File missing in snapshot = empty?
        }
        // Fallback for legacy single-file
        return path === activePath ? replay.artifact.code : "";
    };

    const restoreFileFromSnapshot = (path: string) => {
        const content = getSnapshotContent(path);
        if (content) {
            setFiles(prev => ({
                ...prev,
                [path]: { ...prev[path] || { editable: true }, content } // Ensure editable defaults to true if adding new?
            }));
            addLog(`Restored ${path} from snapshot.`, 'info');
        }
    };

    const restoreReplay = () => {
        // Restore ALL files
        if (!replay) return;
        const snapshot = replay.artifact.workspace_snapshot_json as { path: string, content: string }[];

        if (snapshot) {
            const newFiles = { ...files };
            let restoredCount = 0;
            snapshot.forEach(f => {
                // Only restore if file exists in live workspace OR we want to add it?
                // Plan says "Overlay cannot add new files", so only restore if it exists or allow?
                // Let's allow restore to override content.
                // We should preserve editable flag from LIVE if possible, or snapshot?
                // Snapshot stores editable only.
                // We'll trust snapshot content.
                if (newFiles[f.path]) {
                    newFiles[f.path] = { ...newFiles[f.path], content: f.content };
                    restoredCount++;
                }
            });
            setFiles(newFiles);
            addLog(`Restored ${restoredCount} files from Run #${replay.artifact.run_number}`, 'info');
            setReplay(null);
        } else if (replay.artifact.code) {
            // Legacy Restore
            setFiles(prev => ({
                ...prev,
                [activePath]: { ...prev[activePath], content: replay.artifact.code }
            }));
            addLog(`Code restored from Run #${replay.artifact.run_number}`, 'info');
            setReplay(null);
        }
    };

    // Derived Objectives State (Computed from DISPLAY code)
    const objectivesState = useMemo(() => {
        const targetCode = displayCode || "";
        const state: Record<string, boolean> = {};
        if (quest.objectives) {
            quest.objectives.forEach(obj => {
                let passed = false;
                // Safe access/Normalization
                const validator = obj.validator;

                if (validator) {
                    if (validator.kind === 'contains') {
                        passed = targetCode.includes(validator.value);
                    } else if (validator.kind === 'regex') {
                        try {
                            passed = new RegExp(validator.value, 'm').test(targetCode);
                        } catch (e) { passed = false; }
                    } else if (validator.kind === 'tests_pass') {
                        // Client-side prediction for tests hard, assume false or check last run?
                        // Relying on server result mostly.
                        passed = false;
                    }
                } else {
                    // Fallback for legacy/server-side only objectives (ast, stdout_regex)
                    // We can't validate these purely on client code string easily.
                }
                state[obj.id] = passed;
            });
        }
        return state;
    }, [displayCode, quest.objectives]);

    const passedCount = Object.values(objectivesState).filter(Boolean).length;
    const totalCount = quest.objectives?.length || 0;
    // For local check, allPassed is rough heuristic. Real truth comes from server run.
    // If 'tests_pass' is present, we can't fully validate client-side.
    const hasServerSideObjs = quest.objectives?.some(o => o.validator?.kind === 'tests_pass' || o.validator?.kind === 'ast');
    const allPassed = !hasServerSideObjs && totalCount > 0 && passedCount === totalCount;

    const addLog = (content: string, type: ConsoleEntry['type'] = 'output') => {
        setOutput(prev => [...prev, { type, content, timestamp: Date.now() }]);
    };

    const handleObjectiveClick = (objId: string) => {
        const obj = quest.objectives?.find(o => o.id === objId);
        if (!obj) return;

        const performSearch = (content: string) => {
            const lines = content.split('\n');
            return lines.findIndex((l: string) =>
                obj.validator.kind === 'contains' ? l.includes(obj.validator.value)
                    : obj.validator.kind === 'regex' ? new RegExp(obj.validator.value).test(l) : false
            );
        };

        // 1. Try active file first
        let targetPath = activePath;
        let lineIdx = performSearch(files[activePath]?.content || "");

        // 2. If not found, search other files
        if (lineIdx === -1) {
            for (const [path, file] of Object.entries(files)) {
                if (path === activePath) continue;
                const idx = performSearch(file.content);
                if (idx !== -1) {
                    targetPath = path;
                    lineIdx = idx;
                    break;
                }
            }
        }

        if (lineIdx !== -1) {
            if (targetPath !== activePath) setActivePath(targetPath);
            // Small delay to allow editor to switch content? Monaco React handles this well usually,
            // but we might need a tick.
            setTimeout(() => {
                if (editorRef.current) {
                    editorRef.current.jumpToLine(lineIdx + 1);
                    // TODO: Decorate line?
                }
            }, 50);
        } else {
            addLog(`Objective location not found in workspace.`, 'info');
        }
    };

    const handleCoachAction = async (action: string, tier: string) => {
        if (action === 'dismiss') {
            setCoachData(null);
        } else if (action === 'open_hint') {
            setDrawerTab('hints');
        } else if (action === 'unlock_hint') {
            // Tier Logic: concept->1, guided->2, full_solution->3
            const tierNum = tier === 'concept' ? 1 : tier === 'guided' ? 2 : 3;
            try {
                // Optimistic UI? No, wait for result.
                const res = await unlockHint(quest.slug, tierNum);
                if (res.ok) {
                    addLog(`[COACH] Hint Unlocked! Check Field Manual.`, 'success');
                    setDrawerTab('hints');
                    // Force QuestDrawer to update?
                    (quest as any).hint_tier_unlocked = Math.max((quest as any).hint_tier_unlocked || 0, tierNum);
                } else {
                    addLog(`[COACH] Unlock failed: ${res.reason}`, 'error');
                }
            } catch (e: any) {
                addLog(`[COACH] Error: ${e.message}`, 'error');
            }
        }
    };

    const handleApplyFix = (fix: QuickFix) => {
        if (isReplay || !fix.patch) return;

        const { path, replacement_full_content } = fix.patch;

        // Verify file exists
        if (!files[path]) {
            addLog(`Failed to apply fix: File ${path} not found`, 'error');
            return;
        }

        // Verify file is editable
        if (files[path].editable === false) { // Could be undefined (true)
            addLog(`Failed to apply fix: File ${path} is read-only`, 'error');
            return;
        }

        try {
            setFiles(prev => ({
                ...prev,
                [path]: { ...prev[path], content: replacement_full_content, editable: prev[path]?.editable ?? true }
            }));

            // If file not active, switch to it?
            if (path !== activePath) setActivePath(path);

            setAutosaveStatus('unsaved');
            addLog(`Applied fix: ${fix.title}`, 'success');

            // Only remove on success
            setQuickFixes(prev => prev.filter(f => f.id !== fix.id));
        } catch (e: any) {
            addLog(`Error applying fix: ${e.message}`, 'error');
        }
    };

    const handleNavigateFix = (fix: QuickFix) => {
        if (fix.locator) {
            setActivePath(fix.locator.path);
            setTimeout(() => {
                editorRef.current?.jumpToLine(fix.locator!.line);
            }, 50);
        }
    };

    const handleRun = async () => {
        setIsRunning(true);
        addLog('--- Starting Execution ---', 'info');
        setCoachData(null); // Reset coach

        try {
            const { runQuest } = await import('@/lib/questsApi');

            // Helper to get fresh content from Monaco models to preserve Tabs / exact state
            const getFreshContent = (filePath: string, fallback: string) => {
                const monaco = editorRef.current?.getMonaco();
                if (!monaco) {
                    return fallback;
                }

                const models = monaco.editor.getModels();
                // Find model ending with path (handle / vs \ maybe? usually uri uses /)
                const model = models.find((m: any) => m.uri.path.endsWith(filePath) || m.uri.path.endsWith('/' + filePath));
                return model ? model.getValue() : fallback;
            };

            const workspacePayload = {
                entrypoint: quest.workspace?.entrypoint || activePath,
                files: Object.entries(files).map(([path, f]) => ({
                    path,
                    content: getFreshContent(path, f.content)
                }))
            };

            const result = await runQuest(
                quest.slug,
                "",
                quest.language || "python",
                "execute",
                workspacePayload
            );

            // Show Output
            if (result.stdout) addLog(result.stdout, 'output');
            if (result.stderr) addLog(result.stderr, 'error');

            // Show Test Summary if available
            if (result.test_summary) {
                const ts = result.test_summary;
                if (ts.failed === 0) {
                    addLog(`[TESTS] All ${ts.total} tests passed!`, 'success');
                } else {
                    addLog(`[TESTS] ${ts.failed}/${ts.total} tests failed.`, 'error');
                    ts.failures.forEach((f: any) => addLog(`  - ${f.name}: ${f.message}`, 'error'));
                }
            }

            // Coach Data
            if ((result as any).coach) {
                setCoachData((result as any).coach);
            }
            if ((result as any).debrief) {
                setDebriefData((result as any).debrief);
            }
            setDiagnostics(result.diagnostics || []);
            // Safe fallback for various payload shapes
            const fixes = result.quick_fixes || (result as any).quick_fixes_json || (result as any).attempt?.quick_fixes_json || [];
            if (fixes.length > 0) setQuickFixes(fixes);

            // Add to history if we got an artifact back
            if (result.attempt_id) {
                const newAttempt: QuestAttemptSummary = {
                    id: result.attempt_id,
                    created_at: new Date().toISOString(),
                    run_number: result.run_number || (attempts.length + 1),
                    passed: result.passed,
                    is_submit: false,
                    duration_ms: result.duration_ms || 0,
                    timed_out: result.timed_out || false,
                    exit_code: result.exit_code || 0
                };
                setAttempts(prev => [newAttempt, ...prev]);
            }

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
        setCoachData(null);

        try {
            const { submitQuestSolution } = await import('@/lib/questsApi');
            const { broadcastQuestUpdate } = await import('@/lib/questsEvents');

            // Helper to get fresh content from Monaco models to preserve Tabs / exact state
            const getFreshContent = (filePath: string, fallback: string) => {
                const monaco = editorRef.current?.getMonaco();
                if (!monaco) return fallback;

                const models = monaco.editor.getModels();
                const model = models.find((m: any) => m.uri.path.endsWith(filePath) || m.uri.path.endsWith('/' + filePath));
                return model ? model.getValue() : fallback;
            };

            const workspacePayload = {
                entrypoint: quest.workspace?.entrypoint || activePath,
                files: Object.entries(files).map(([path, f]) => ({
                    path,
                    content: getFreshContent(path, f.content)
                }))
            };

            const result = await submitQuestSolution(
                quest.slug,
                "",
                quest.language || "python",
                workspacePayload
            );

            if ((result as any).coach) {
                setCoachData((result as any).coach);
            }
            if (result.debrief) {
                setDebriefData(result.debrief);
            }
            setDiagnostics(result.diagnostics || []);
            const fixes = result.quick_fixes || (result as any).quick_fixes_json || (result as any).attempt?.quick_fixes_json || [];
            if (fixes.length > 0) setQuickFixes(fixes);

            if (result.ok) {
                // 1. Notify UI components (QuestBoard)
                // broadcastQuestUpdate(result.quest); // Result doesn't have quest?
                // Actually broadcastQuestUpdate expects QuestSummary.
                // We might need to fetch it or construct it? 
                // Or just refresh world progress.

                // 2. Success Overlay
                setShowSuccess(true);
            } else {
                addLog('Submission rejected by server.', 'error');
            }
        } catch (e: any) {
            addLog(`Submission Error: ${e.message}`, 'error');
        }
    };

    // Auto-save (Files Map)
    useEffect(() => {
        if (autosaveStatus === 'unsaved') {
            setAutosaveStatus('saving');
            const key = `evalforge:workspace:${quest.id}`;
            localStorage.setItem(key, JSON.stringify(files));
            const t = setTimeout(() => setAutosaveStatus('saved'), 800);
            return () => clearTimeout(t);
        }
    }, [files, quest.id, autosaveStatus]);

    // Restore
    useEffect(() => {
        const key = `evalforge:workspace:${quest.id}`;
        const saved = localStorage.getItem(key);
        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                // Merge with default logic to keep editable flags if missing?
                // For now assumes complete override
                setFiles(prev => ({ ...prev, ...parsed }));
            } catch (e) {
                console.error("Failed to restore workspace", e);
            }
        }
    }, [quest.id]);

    const resetCode = () => {
        if (quest.workspace) {
            const initial: Record<string, { content: string; editable: boolean }> = {};
            quest.workspace.files.forEach(f => {
                initial[f.path] = { content: f.content, editable: f.editable ?? true };
            });
            setFiles(initial);
        } else {
            // Re-run the initial logic
            const ext = quest.language || 'python';
            let name = 'main.py';
            if (quest.language === 'typescript') name = 'main.ts';
            if (quest.language === 'javascript') name = 'main.js';
            // ... etc, actually reusing logic is better but copy for now
            const content = quest.starter_code || "";
            setFiles({ [name]: { content, editable: true } });
        }
        addLog("Workspace reset to original state.", "info");
    };

    return (
        <div className="h-full flex flex-col bg-black/40 rounded-xl border border-zinc-800 overflow-hidden shadow-inner relative">

            {showSuccess && (
                <QuestSuccessOverlay
                    quest={quest}
                    debrief={debriefData}
                    onClose={() => setShowSuccess(false)}
                    onNext={(slug) => {
                        setShowSuccess(false);
                        if (slug) {
                            navigate(`/arcade/worlds/${worldSlug}/quests/${slug}`);
                        } else {
                            onBack?.();
                        }
                    }}
                />
            )}

            {/* Header */}
            {isReplay && (
                <div className="h-10 bg-amber-950/80 border-b border-amber-500/30 flex items-center justify-between px-4 animate-in fade-in slide-in-from-top-2">
                    <div className="flex items-center gap-2 text-amber-200 text-xs font-mono font-bold">
                        <HistoryIcon className="w-3 h-3" />
                        <span>REPLAYING RUN #{replay?.artifact.run_number}</span>
                        <div className="px-1.5 py-0.5 bg-amber-500/20 text-amber-300 rounded text-[9px] uppercase tracking-wider border border-amber-500/30">Snapshot</div>
                        <span className="text-amber-500/50">|</span>
                        <span className="opacity-75">READ ONLY (RESTORE TO EDIT)</span>
                    </div>

                    <div className="flex items-center gap-2">
                        <button
                            onClick={handleExportReport}
                            className="px-2 py-1 text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800 rounded transition-all flex items-center gap-1"
                            title="Export Run Report"
                        >
                            <Download className="w-3 h-3" />
                        </button>
                        <button
                            onClick={() => {
                                setDiffFile(activePath);
                                setShowDiff(true);
                            }}
                            className="px-3 py-1 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-[10px] font-bold uppercase tracking-wider rounded border border-zinc-700 transition-all flex items-center gap-1"
                        >
                            <Split className="w-3 h-3" /> Diff vs Live
                        </button>
                        <button
                            onClick={restoreReplay}
                            className="px-3 py-1 bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 text-[10px] font-bold uppercase tracking-wider rounded border border-amber-500/30 transition-all flex items-center gap-1"
                        >
                            <FileCode className="w-3 h-3" /> Restore All
                        </button>
                        <button
                            onClick={handleRun} // Runs THIS replay code as new attempt
                            className="px-3 py-1 bg-cyan-900/30 hover:bg-cyan-900/50 text-cyan-400 text-[10px] font-bold uppercase tracking-wider rounded border border-cyan-500/30 transition-all flex items-center gap-1"
                        >
                            <Play className="w-3 h-3" /> Rerun
                        </button>
                        <button
                            onClick={exitReplay}
                            className="px-3 py-1 hover:bg-zinc-800 text-zinc-400 hover:text-white text-[10px] font-bold uppercase tracking-wider rounded transition-all"
                        >
                            Exit
                        </button>
                    </div>
                </div>
            )}


            {/* Diff Modal */}
            {
                showDiff && (
                    <div className="absolute inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-8 animate-in fade-in duration-200">
                        <div className="bg-zinc-900 border border-zinc-700 w-full h-full max-w-6xl max-h-[800px] rounded-xl shadow-2xl flex flex-col overflow-hidden">
                            <div className="h-10 border-b border-zinc-800 flex items-center justify-between px-4 bg-zinc-950">
                                <div className="flex items-center gap-4">
                                    <span className="text-zinc-400 font-bold text-xs uppercase tracking-wider">Diff View</span>
                                    <select
                                        value={diffFile}
                                        onChange={e => setDiffFile(e.target.value)}
                                        className="bg-zinc-800 text-zinc-200 text-xs rounded px-2 py-1 border border-zinc-700 focus:outline-none focus:ring-1 focus:ring-cyan-500"
                                    >
                                        {Object.keys(files).map(f => <option key={f} value={f}>{f}</option>)}
                                    </select>
                                </div>
                                <div className="flex items-center gap-2">
                                    <button
                                        onClick={() => restoreFileFromSnapshot(diffFile)}
                                        className="px-3 py-1 bg-amber-500/20 hover:bg-amber-500/30 text-amber-400 text-xs rounded border border-amber-500/30 flex items-center gap-1"
                                    >
                                        <RotateCcw className="w-3 h-3" /> Restore {diffFile}
                                    </button>
                                    <button onClick={() => setShowDiff(false)} className="text-zinc-500 hover:text-white"><X className="w-5 h-5" /></button>
                                </div>
                            </div>
                            <div className="flex-1 min-h-0">
                                <DiffEditor
                                    original={getSnapshotContent(diffFile)}
                                    modified={files[diffFile]?.content || ""}
                                    language={quest.language || 'python'}
                                    theme="vs-dark"
                                    options={{
                                        readOnly: true,
                                        renderSideBySide: true,
                                        minimap: { enabled: false }
                                    }}
                                />
                            </div>
                            <div className="h-6 bg-zinc-950 border-t border-zinc-800 flex items-center justify-center text-[10px] text-zinc-600 gap-8">
                                <span className="flex items-center gap-2"><div className="w-2 h-2 bg-red-900/50 rounded-full"></div> Run #{replay?.artifact.run_number} (Snapshot)</span>
                                <span className="flex items-center gap-2"><div className="w-2 h-2 bg-green-900/50 rounded-full"></div> Live Workspace (Current)</span>
                            </div>
                        </div>
                    </div>
                )
            }

            <div className="h-14 border-b border-zinc-800 bg-zinc-900/80 backdrop-blur-md flex items-center justify-between px-4 shrink-0">
                <div className="flex items-center gap-4">
                    <button onClick={onBack} className="text-zinc-500 hover:text-zinc-300 transition-colors">
                        ←
                    </button>
                    <div>
                        <div className="text-xs font-bold text-zinc-500 uppercase tracking-widest leading-none mb-1">Mission Control</div>
                        <div className="flex items-center gap-3">
                            <span className="text-sm font-bold text-cyan-100">{quest.title}</span>
                            {(quest.state === 'completed' || quest.state === 'mastered') && (
                                <div title="Previously completed" className="flex items-center gap-1.5 px-2 py-0.5 bg-cyan-950/30 border border-cyan-800/50 rounded-full">
                                    <Check className="w-3 h-3 text-cyan-400" />
                                    <span className="text-[9px] font-bold text-cyan-500 uppercase tracking-widest">Done</span>
                                </div>
                            )}
                            <div className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wide border ${allPassed ? 'bg-emerald-950/40 text-emerald-400 border-emerald-500/30' : 'bg-zinc-900 text-zinc-500 border-zinc-700'}`}>
                                {passedCount}/{totalCount} Objectives
                            </div>
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-2">
                    <button
                        onClick={toggleFocusMode}
                        className={`p-2 rounded-lg transition-all border ${focusMode ? 'text-cyan-400 bg-cyan-950/30 border-cyan-800/50' : 'text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800 border-transparent'}`}
                        title={focusMode ? "Exit Focus Mode" : "Enter Focus Mode"}
                    >
                        {focusMode ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
                    </button>

                    {!isReplay && (
                        <div className="flex items-center gap-2">
                            <span className={`text-[10px] uppercase tracking-wider font-bold transition-colors ${autosaveStatus === 'saving' ? 'text-amber-500' :
                                autosaveStatus === 'unsaved' ? 'text-zinc-500' : 'text-zinc-600'
                                }`}>
                                {autosaveStatus === 'saving' ? 'Saving...' :
                                    autosaveStatus === 'unsaved' ? 'Unsaved' :
                                        'Autosaved'}
                            </span>
                            <button
                                onClick={resetCode}
                                className="p-2 text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800 rounded-lg transition-all"
                                title="Reset Code"
                            >
                                <RotateCcw className="w-4 h-4" />
                            </button>
                        </div>
                    )}

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
                        disabled={!allPassed || isRunning || isReplay}
                        title={isReplay ? "Exit replay to submit" : ""}
                        className={`
                            flex items-center gap-2 px-6 py-2 rounded-lg text-xs font-bold uppercase tracking-widest transition-all shadow-lg
                            ${allPassed && !isReplay
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
                <div className="hidden lg:flex flex-col border-r border-zinc-800 bg-zinc-950/30 min-h-0">
                    <div className="flex-1 overflow-y-auto">
                        {/* File Explorer if multiple files */}
                        {Object.keys(files).length > 1 && (
                            <div className="border-b border-zinc-800/50 p-2">
                                <div className="text-[10px] font-bold uppercase tracking-wider text-zinc-500 mb-2 px-2">Workspace</div>
                                <div className="space-y-0.5">
                                    {Object.keys(files).sort().map(path => (
                                        <button
                                            key={path}
                                            onClick={() => setActivePath(path)}
                                            className={`w-full text-left px-3 py-1.5 rounded text-xs font-mono flex items-center justify-between group transition-all
                                                ${activePath === path
                                                    ? 'bg-cyan-950/30 text-cyan-300 border border-cyan-900/50'
                                                    : 'text-zinc-400 hover:bg-zinc-900/50 hover:text-zinc-200 border border-transparent'
                                                }`}
                                        >
                                            <span className="flex items-center gap-2">
                                                {!files[path].editable ? <Lock className="w-3 h-3 opacity-50" /> : <FileCode className="w-3 h-3 opacity-75" />}
                                                <span className={!files[path].editable ? "opacity-75" : ""}>{path}</span>
                                                {files[path].editable && files[path].content !== baseFiles[path] && (
                                                    <span className="w-1.5 h-1.5 rounded-full bg-amber-400/80" />
                                                )}
                                            </span>
                                            {!files[path].editable && <span className="text-[9px] opacity-30 uppercase">Lock</span>}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        )}

                        <QuestDrawer
                            quest={quest}
                            objectivesState={objectivesState}
                            onObjectiveClick={handleObjectiveClick}
                            attempts={attempts}
                            onSelectAttempt={handleReplay}
                            controlTab={drawerTab}
                            onTabChange={setDrawerTab}
                            customPanels={{
                                tutorial: quest.tutorial_md ? (
                                    <TutorialPanel
                                        tutorialMd={quest.tutorial_md}
                                        keyTerms={quest.key_terms || []}
                                        codexRefs={quest.codex_references || []}
                                        onOpenCodexRef={handleOpenCodex}
                                        onPasteCode={Object.keys(files).length === 1 ? (code) => {
                                            const path = Object.keys(files)[0];
                                            if (!path) return;

                                            setFiles(prev => ({
                                                ...prev,
                                                [path]: { ...prev[path], content: code }
                                            }));
                                            setAutosaveStatus('unsaved');
                                            addLog(`Pasted code into ${path}`, 'info');
                                        } : undefined}
                                    />
                                ) : null
                            }}
                        />
                    </div>
                </div>

                {/* Editor Side */}
                <div className="h-full min-h-0 grid grid-rows-[minmax(0,1fr)_minmax(320px,1fr)] gap-2 bg-zinc-950 relative">
                    <div className="min-h-0 relative flex flex-col">
                        {/* Tab Bar if multiple files */}
                        {Object.keys(files).length > 1 && (
                            <div className="flex items-center border-b border-zinc-800 bg-black/40 overflow-x-auto hide-scrollbar shrink-0">
                                {Object.keys(files).sort().map(path => (
                                    <button
                                        key={path}
                                        onClick={() => setActivePath(path)}
                                        className={`flex-shrink-0 px-4 py-2 text-xs font-mono border-r border-zinc-800 transition-colors flex items-center gap-2
                                             ${activePath === path
                                                ? 'bg-zinc-900 text-zinc-200 border-t-2 border-t-cyan-500'
                                                : 'text-zinc-500 hover:text-zinc-300 hover:bg-zinc-900/50 border-t-2 border-t-transparent'
                                            }`}
                                    >
                                        {!files[path].editable && <Lock className="w-3 h-3 opacity-50" />}
                                        {path}
                                        {files[path].editable && files[path].content !== baseFiles[path] && (
                                            <span className="text-amber-400">●</span>
                                        )}
                                    </button>
                                ))}
                            </div>
                        )}

                        <div className="flex-1 min-h-0 relative">
                            <QuestEditor
                                ref={editorRef}
                                value={displayCode || ""} // Show replay code or active file
                                path={activePath}
                                onChange={v => {
                                    if (!isReplay && files[activePath]?.editable) {
                                        setFiles(prev => ({
                                            ...prev,
                                            [activePath]: { ...prev[activePath], content: v }
                                        }));
                                        setAutosaveStatus('unsaved');
                                    }
                                }}
                                language={
                                    // Naive lang detection
                                    activePath.endsWith('.ts') ? 'typescript' :
                                        activePath.endsWith('.js') ? 'javascript' :
                                            activePath.endsWith('.css') ? 'css' :
                                                activePath.endsWith('.html') ? 'html' :
                                                    activePath.endsWith('.json') ? 'json' :
                                                        quest.language || "python"
                                }
                                isSaving={autosaveStatus === 'saving'}
                                readOnly={isReadOnly}
                                diagnostics={diagnostics.filter(d => d.path === activePath)}
                            />
                        </div>
                        {/* Problems Panel */}
                        <ProblemsPanel
                            diagnostics={diagnostics}
                            onDiagnosticClick={(path, line) => {
                                setActivePath(path);
                                setTimeout(() => {
                                    editorRef.current?.jumpToLine(line);
                                }, 50);
                            }}
                        />

                        {/* Coach Banner */}
                        <div className="shrink-0 z-20">
                            <AnimatePresence>
                                {coachData && (
                                    <CoachBanner
                                        coach={coachData}
                                        onAction={handleCoachAction}
                                    />
                                )}
                            </AnimatePresence>
                        </div>
                    </div>

                    <div className="flex flex-col min-h-0">
                        <QuickFixBar
                            fixes={quickFixes}
                            onApplyPatch={handleApplyFix}
                            onNavigate={handleNavigateFix}
                            readOnly={isReadOnly}
                        />

                        {/* Rich Console */}
                        <div className="flex-1 border-t border-zinc-800 bg-[#09090b] flex flex-col shrink-0 font-mono min-h-0">
                            <div className="px-3 py-1.5 border-b border-zinc-800/50 flex justify-between items-center bg-black/20 shrink-0">
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

            {/* Codex Drawer (Phase 9.1) */}
            <CodexDrawer
                isOpen={codexOpen}
                activeRef={codexRef}
                onClose={() => setCodexOpen(false)}
                onOpenCodex={handleOpenCodex}
                questSlug={quest.slug}
            />
        </div>
    );
}

export function QuestIDEPage() {
    const { questId } = useParams<{ questId: string }>();
    const navigate = useNavigate();
    const [quest, setQuest] = useState<QuestSummary | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!questId) return;
        setLoading(true);
        fetchQuest(questId)
            .then(setQuest)
            .catch(err => setError(err.message))
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
    }, [questId]);

    if (loading) {
        return (
            <div className="h-full flex flex-col items-center justify-center gap-2 text-zinc-500">
                <div className="w-4 h-4 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
                <span className="text-xs font-mono">LOADING LINK...</span>
            </div>
        );
    }

    if (error || !quest) {
        return (
            <div className="h-full flex flex-col items-center justify-center gap-4 text-center">
                <div className="flex flex-col items-center gap-2">
                    <AlertTriangle className="w-8 h-8 text-amber-500/50" />
                    <div className="text-amber-400 font-bold">UPLINK FAILED</div>
                    <div className="text-xs text-white/50">{error || "Signal lost."}</div>
                </div>
                <button
                    onClick={() => navigate('..')}
                    className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-xs text-zinc-300 rounded border border-zinc-700"
                >
                    Return to Board
                </button>
            </div>
        );
    }

    return (
        <QuestIDE
            quest={quest}
            onBack={() => navigate('..')}
        />
    );
}
