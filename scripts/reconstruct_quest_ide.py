import re

with open(r"d:\EvalForge\apps\web\src\components\quests\QuestIDE.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Imports
imports = """import { ToastAction } from '@radix-ui/react-toast';
import { CodexDrawer } from '../codex/CodexDrawer';
import { BossHud } from '../oracle/BossHud';
import { IntentOracleEvalButton } from '../oracle/IntentOracleEvalButton';
import { CoachPanel } from './CoachPanel';

interface QuestIDEProps {"""
content = re.sub(r"import \{ ToastAction \} from '@radix-ui/react-toast';\s+interface QuestIDEProps \{", imports, content)
if "CoachPanel" not in content and "interface QuestIDEProps" in content:
    # fallback
    content = re.sub(r"interface QuestIDEProps \{", imports, content)


# 2. State
state_replace = """    // Query Inspector / Terminal State
    const [activeTerminalTab, setActiveTerminalTab] = useState<'terminal' | 'trace' | 'result' | 'explain_plan' | 'explain_coach' | 'results' | 'debug' | 'raw' | 'oracle'>(() => {
        const saved = localStorage.getItem(`terminalTab:${initialQuest.slug}`);
        return (saved as any) || 'terminal';
    });

    useEffect(() => {
        localStorage.setItem(`terminalTab:${quest.slug}`, activeTerminalTab);
    }, [activeTerminalTab, quest.slug]);

    // Codex State
    const [codexOpen, setCodexOpen] = useState(false);

    useEffect(() => {
        const panel = new URLSearchParams(location.search).get("panel");
        if (panel === "codex") setCodexOpen(true);
    }, [location.search]);

    const handleOpenCodex = (ref: string) => {
        console.log('📖 NAVIGATING TO CODEX:', ref);
        const params = new URLSearchParams(window.location.search);
        params.set('panel', 'codex');
        params.set('term', ref);
        const newUrl = `${window.location.pathname}?${params.toString()}`;
        window.history.replaceState(null, '', newUrl);
        navigate(`${window.location.pathname}?${params.toString()}`, { replace: true });
    };"""

content = re.sub(r"    // Query Inspector / Terminal State.*?const handleOpenCodex = \(ref: string\) => \{.*?navigate\(`\$\{window\.location\.pathname\}\?\$\{params\.toString\(\)\}`, \{ replace: true \}\);\n    \};", state_replace, content, flags=re.DOTALL)


# 3. Handle run
handle_run_replace = """            if (result.test_summary) {
                const ts = result.test_summary;
                if (ts.failed === 0) {
                    addLog(`[TESTS] All ${ts.total} tests passed!`, 'success');
                } else {
                    addLog(`[TESTS] ${ts.failed}/${ts.total} tests failed.`, 'error');
                    ts.failures.forEach((f: any) => addLog(`  - ${f.name}: ${f.message}`, 'error'));
                    addLog("💡 Tip: Open the 'Debug' panel for analysis.", "info");
                    setActiveTerminalTab('results');
                }
            } else if (result.stderr || result.error) {
                setActiveTerminalTab('results');
            }"""
content = re.sub(r"            if \(result\.test_summary\) \{.*?\}", handle_run_replace, content, flags=re.DOTALL, count=1)


# 4. Entrypoint chip
chip = """                        <div className="flex-1 min-h-0 relative">
                            {/* Entrypoint Chip */}
                            {activePath !== (quest.workspace?.entrypoint || (quest.language === 'sql' ? 'task.sql' : 'main.py')) && (
                                <div className="absolute top-2 right-4 z-10 flex animate-in fade-in zoom-in-95 duration-200">
                                    <button 
                                        onClick={() => setActivePath(quest.workspace?.entrypoint || (quest.language === 'sql' ? 'task.sql' : 'main.py'))}
                                        className="flex items-center gap-2 px-3 py-1.5 bg-amber-500/10 border border-amber-500/30 text-amber-500 rounded-full text-xs font-mono shadow-lg hover:bg-amber-500/20 transition-colors cursor-pointer"
                                    >
                                        <AlertTriangle className="w-3 h-3" />
                                        Entrypoint: {quest.workspace?.entrypoint || (quest.language === 'sql' ? 'task.sql' : 'main.py')}
                                    </button>
                                </div>
                            )}

                            <QuestEditor"""
content = content.replace('                        <div className="flex-1 min-h-0 relative">\n                            <QuestEditor', chip)


# 5. Tab Buttons
tabs = """                                    {quest.language === 'sql' && (
                                        <>
                                            <button
                                                onClick={() => setActiveTerminalTab('result')}
                                                className={`px-4 py-2 text-[10px] uppercase font-bold tracking-widest flex items-center gap-2 border-b-2 transition-colors whitespace-nowrap
                                                    ${activeTerminalTab === 'result' ? 'text-workshop-cyan border-workshop-cyan bg-cyan-950/20' : 'text-zinc-500 border-transparent hover:text-zinc-300 hover:bg-zinc-900/50'}`}
                                            >
                                                <Table2 className="w-3 h-3" /> Query Result
                                            </button>
                                            <button
                                                onClick={() => setActiveTerminalTab('trace')}
                                                className={`px-4 py-2 text-[10px] uppercase font-bold tracking-widest flex items-center gap-2 border-b-2 transition-colors whitespace-nowrap
                                                    ${activeTerminalTab === 'trace' ? 'text-workshop-cyan border-workshop-cyan bg-cyan-950/20' : 'text-zinc-500 border-transparent hover:text-zinc-300 hover:bg-zinc-900/50'}`}
                                            >
                                                <TerminalSquare className="w-3 h-3" /> Trace
                                            </button>
                                            <button
                                                onClick={() => setActiveTerminalTab('explain_plan')}
                                                className={`px-4 py-2 text-[10px] uppercase font-bold tracking-widest flex items-center gap-2 border-b-2 transition-colors whitespace-nowrap
                                                    ${activeTerminalTab === 'explain_plan' ? 'text-workshop-cyan border-workshop-cyan bg-cyan-950/20' : 'text-zinc-500 border-transparent hover:text-zinc-300 hover:bg-zinc-900/50'}`}
                                            >
                                                <Layers className="w-3 h-3" /> Explain (Plan)
                                            </button>
                                        </>
                                    )}
                                    <button
                                        onClick={() => setActiveTerminalTab('results')}
                                        className={`px-4 py-2 text-[10px] uppercase font-bold tracking-widest flex items-center gap-2 border-b-2 transition-colors whitespace-nowrap
                                            ${activeTerminalTab === 'results' ? 'text-amber-400 border-amber-400 bg-amber-950/20' : 'text-zinc-500 border-transparent hover:text-zinc-300 hover:bg-zinc-900/50'}`}
                                    >
                                        <CheckCircle2 className="w-3 h-3" /> Results
                                    </button>
                                    <button
                                        onClick={() => setActiveTerminalTab('explain_coach')}
                                        className={`px-4 py-2 text-[10px] uppercase font-bold tracking-widest flex items-center gap-2 border-b-2 transition-colors whitespace-nowrap
                                            ${activeTerminalTab === 'explain_coach' ? 'text-indigo-400 border-indigo-400 bg-indigo-950/20' : 'text-zinc-500 border-transparent hover:text-zinc-300 hover:bg-zinc-900/50'}`}
                                    >
                                        <Sparkles className="w-3 h-3" /> Explain (Coach)
                                    </button>
                                    <button
                                        onClick={() => setActiveTerminalTab('debug')}
                                        className={`px-4 py-2 text-[10px] uppercase font-bold tracking-widest flex items-center gap-2 border-b-2 transition-colors whitespace-nowrap
                                            ${activeTerminalTab === 'debug' ? 'text-orange-400 border-orange-400 bg-orange-950/20' : 'text-zinc-500 border-transparent hover:text-zinc-300 hover:bg-zinc-900/50'}`}
                                    >
                                        <Bug className="w-3 h-3" /> Debug
                                    </button>
                                    <button
                                        onClick={() => setActiveTerminalTab('oracle')}
                                        className={`px-4 py-2 text-[10px] uppercase font-bold tracking-widest flex items-center gap-2 border-b-2 transition-colors whitespace-nowrap
                                            ${activeTerminalTab === 'oracle' ? 'text-purple-400 border-purple-400 bg-purple-950/20' : 'text-zinc-500 border-transparent hover:text-zinc-300 hover:bg-zinc-900/50'}`}
                                    >
                                        <Eye className="w-3 h-3" /> Intent Oracle
                                    </button>
                                    {import.meta.env.DEV && (
                                        <button
                                            onClick={() => setActiveTerminalTab('raw')}
                                            className={`px-4 py-2 text-[10px] uppercase font-bold tracking-widest flex items-center gap-2 border-b-2 transition-colors whitespace-nowrap
                                                ${activeTerminalTab === 'raw' ? 'text-zinc-300 border-zinc-500 bg-zinc-800/50' : 'text-zinc-600 border-transparent hover:text-zinc-400 hover:bg-zinc-900/50'}`}
                                        >
                                            <Code2 className="w-3 h-3" /> Raw
                                        </button>
                                    )}"""
content = re.sub(r"                                    \{quest\.language === 'sql' && \(.*?Explain\n                                            </button>\n                                        </>\n                                    \)}", tabs, content, flags=re.DOTALL)

# 6. Content Panes
panes = """                                {(['result', 'trace', 'explain_plan'].includes(activeTerminalTab)) && (
                                    <div className="h-full overflow-hidden">
                                        {quest.language === 'sql' ? (
                                            <QueryInspector activeTabOverride={activeTerminalTab === 'explain_plan' ? 'explain' : activeTerminalTab as any} />
                                        ) : (
                                            <div className="flex items-center justify-center p-8 text-zinc-500 text-xs italic">
                                                Inspector not available for this language.
                                            </div>
                                        )}
                                    </div>
                                )}

                                {activeTerminalTab === 'results' && (
                                    <div className="h-full overflow-y-auto p-4 space-y-4">
                                        <h4 className="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-2">Objective Verification</h4>
                                        <div className="space-y-2">
                                            {quest.objectives?.map((obj) => (
                                                <button
                                                    key={obj.id}
                                                    onClick={() => handleObjectiveClick(obj.id)}
                                                    className={`w-full text-left p-3 rounded-lg border bg-zinc-900/40 hover:bg-zinc-800/60 transition-colors group relative overflow-hidden flex items-start gap-3
                                                        ${objectivesState[obj.id] ? 'border-emerald-500/30 shadow-[0_0_15px_rgba(16,185,129,0.05)]' : 'border-zinc-800 hover:border-zinc-700'}
                                                    `}
                                                >
                                                    <div className="mt-0.5 shrink-0">
                                                        {objectivesState[obj.id] ? (
                                                            <CheckCircle2 className="w-4 h-4 text-emerald-500 drop-shadow-[0_0_8px_rgba(16,185,129,0.5)]" />
                                                        ) : (
                                                            <div className="w-4 h-4 rounded-full border-2 border-zinc-700 bg-zinc-900 shadow-inner" />
                                                        )}
                                                    </div>
                                                    <div className="flex-1 min-w-0">
                                                        <span className={cn(
                                                            "text-xs font-mono block mb-0.5 leading-tight",
                                                            objectivesState[obj.id] ? "text-emerald-200" : "text-zinc-300"
                                                        )}>
                                                            {(obj as any).text || (obj as any).title || <span className="opacity-40 italic">(missing text)</span>}
                                                        </span>
                                                        {obj.why && (
                                                            <span className="text-[10px] text-zinc-500 block leading-tight">
                                                                {obj.why}
                                                            </span>
                                                        )}
                                                    </div>
                                                </button>
                                            ))}
                                            {!quest.objectives?.length && (
                                                <div className="text-xs text-zinc-500 italic p-4 text-center border border-zinc-800 rounded-lg">No objectives listed.</div>
                                            )}
                                        </div>
                                    </div>
                                )}

                                {activeTerminalTab === 'debug' && (
                                    <CoachPanel mode="debug" quest={quest} lastRunResult={lastRunResult} attemptId={lastRunResult?.attempt?.id} workspaceFiles={files} />
                                )}

                                {activeTerminalTab === 'explain_coach' && (
                                    <CoachPanel mode="explain" quest={quest} lastRunResult={lastRunResult} attemptId={lastRunResult?.attempt?.id} workspaceFiles={files} />
                                )}

                                {activeTerminalTab === 'raw' && import.meta.env.DEV && (
                                    <div className="h-full overflow-y-auto p-4 bg-zinc-950/50 font-mono text-[10px]">
                                        <div className="space-y-4">
                                            <div>
                                                <h4 className="text-amber-500 font-bold uppercase mb-1">Raw Run Payload</h4>
                                                <div className="bg-black/50 p-2 rounded border border-zinc-800 text-zinc-400 whitespace-pre-wrap overflow-x-auto">
                                                    {lastRunResult ? JSON.stringify(lastRunResult, null, 2) : "No run recorded yet in this session."}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                )}

                                {activeTerminalTab === 'oracle' && (
                                    <div className="h-full overflow-y-auto p-4 space-y-6">
                                        <div className="max-w-xl mx-auto space-y-4">
                                            <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/50">
                                                <BossHud />
                                            </div>
                                            <IntentOracleEvalButton />
                                        </div>
                                    </div>
                                )}"""

content = re.sub(r"                                \{\(\['result', 'trace', 'explain'\]\.includes.*?\}", panes, content, flags=re.DOTALL)


# 7. Add CodexDrawer to end
drawer = """            </div>
            
            <CodexDrawer
                isOpen={codexOpen}
                activeRef={new URLSearchParams(location.search).get("term") || 'codex:home'}
                onClose={() => {
                    setCodexOpen(false);
                    const params = new URLSearchParams(location.search);
                    params.delete('panel');
                    params.delete('term');
                    navigate(`${location.pathname}?${params.toString()}`, { replace: true });
                }}
                onOpenCodex={handleOpenCodex}
                questSlug={quest.slug}
            />
        </div>
    );
}

export function QuestIDEPage() {"""
content = content.replace('            </div>\n        </div>\n    );\n}\n\nexport function QuestIDEPage() {', drawer)


if "import { cn }" not in content:
    content = content.replace("import { AnimatePresence", "import { cn } from '@/lib/utils';\nimport { AnimatePresence")


with open(r"d:\EvalForge\apps\web\src\components\quests\QuestIDE.tsx", "w", encoding="utf-8") as f:
    f.write(content)
