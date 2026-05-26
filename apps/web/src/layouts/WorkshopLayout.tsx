// Sprint 22: useCurrentLayout replaced with useSettingsStore.worldViewMode.
// isCyberdeck / isOrion removed — Workshop is the only layout.
// Sprint 22.6: worldViewMode/Map toggle rolled back — OrionMap data flow was unwired.
// Board view is the only world-selection view.
import React, { useEffect } from "react";
import { openWorkshopGuide } from "../features/workshop/useWorkshopTips";
import { PracticeGauntletCard } from "../components/practice/PracticeGauntletCard";
import { useParams, useSearchParams, Link } from "react-router-dom";
import { useQuestStore, QuestState } from "../store/questStore";
import { useGameStore } from "../store/gameStore";
import { useSettingsStore } from "../store/settingsStore";
import { cn } from "../lib/utils";
import { EyeIcon, BookOpen, BarChart2 } from "lucide-react";
import { WorkshopToolsPanel } from "../components/workshop/WorkshopToolsPanel";
import { PanelId } from "../features/workshop/workshopPanels";
import { CodexDrawer } from "../components/codex/CodexDrawer";
// Sprint 22.6: OrionMap import removed — Map toggle rolled back. OrionMap.tsx deleted.

// Re-export type for compatibility, though we use PanelId internally now
export type WorkshopMode = PanelId | 'quest'; // 'quest' is legacy default, mapped to a panel or ignored

interface WorkshopLayoutProps {
    bossHud: React.ReactNode;
    worldSelector: React.ReactNode;
    questPanel: React.ReactNode;
    projectPanel: React.ReactNode;
    codexPanel: React.ReactNode;
    activityFeed: React.ReactNode;
    extraTopRight?: React.ReactNode;

    /** Latest integrity delta from combat (negative = you took damage). */
    integrityDelta?: number | null;
    /** Latest boss HP delta from combat (negative = boss took damage). */
    bossHpDelta?: number | null;

    // Mode Control (Now Panel Control)
    currentMode?: WorkshopMode;
    onModeChange?: (mode: WorkshopMode) => void;
    hasSkill?: (skill: string) => boolean;
}

type BenchHit = "none" | "player" | "boss" | "both";

function WorkbenchHeader({ onGuide }: { onGuide?: () => void }) {
    return (
        <div className="flex items-center justify-between px-1">
            <h2 className="text-xs font-semibold uppercase tracking-[0.2em] text-workshop-subtle">
                Workbench
            </h2>
            <button
                onClick={onGuide}
                className="text-[10px] text-workshop-cyan hover:underline"
            >
                ? Help
            </button>
        </div>
    );
}

export const WorkshopLayout: React.FC<WorkshopLayoutProps> = ({
    bossHud,
    worldSelector,
    questPanel,
    projectPanel,
    codexPanel,
    activityFeed,
    extraTopRight,
    integrityDelta,
    bossHpDelta,
    currentMode = 'judge',
    onModeChange,
    hasSkill = () => false,
}) => {
    // 1. Route Context
    const params = useParams<{ worldSlug?: string; questId?: string; bossSlug?: string }>();
    const [searchParams, setSearchParams] = useSearchParams();

    // "Workbench" state = inside a quest. "List" state = board/index.
    const isWorkbench = Boolean(params.questId);

    // Panel State (URL Driven)
    const activePanelStr = searchParams.get('panel');
    const activePanel = (activePanelStr && ['judge', 'explain', 'debug', 'codex'].includes(activePanelStr))
        ? (activePanelStr as PanelId)
        : 'judge';

    const handlePanelChange = (p: PanelId) => {
        setSearchParams(prev => {
            const copy = new URLSearchParams(prev);
            copy.set('panel', p);
            return copy;
        });
        onModeChange?.(p);
    };

    // Store Actions
    const setActiveWorld = useQuestStore((s: QuestState) => s.setActiveWorldSlug);
    const setActiveTrack = useQuestStore((s: QuestState) => s.setActiveTrackId);
    const setActiveBoss = useQuestStore((s: QuestState) => s.setActiveBossSlug);
    const activeTrack = useGameStore((s) => s.activeTrack);

    useEffect(() => {
        const worldSlug = params.worldSlug || searchParams.get('world');
        const trackId = params.questId || searchParams.get('track');
        const bossSlug = params.bossSlug;

        if (worldSlug) setActiveWorld(worldSlug);
        if (trackId) setActiveTrack(trackId);
        if (bossSlug) setActiveBoss(bossSlug);

    }, [params.worldSlug, params.questId, params.bossSlug, searchParams, setActiveWorld, setActiveTrack, setActiveBoss]);

    // Extract Codex Term from URL
    const activeCodexTerm = searchParams.get('term') || undefined;
    const codexIsOpen = activePanel === 'codex' || !!activeCodexTerm;

    const handleCodexClose = () => {
        setSearchParams(prev => {
            const copy = new URLSearchParams(prev);
            // Revert to 'judge' if panel was codex, or leave as is if they just had term set
            if (copy.get('panel') === 'codex') copy.set('panel', 'judge');
            copy.delete('term');
            return copy;
        });
    };

    const handleOpenCodex = (ref: string) => {
        setSearchParams(prev => {
            const copy = new URLSearchParams(prev);
            copy.set('panel', 'codex');
            copy.set('term', ref);
            return copy;
        });
    };

    // Local state for hit effects only
    const [benchHit, setBenchHit] = React.useState<BenchHit>("none");
    const [activityHit, setActivityHit] = React.useState<"none" | "tick">("none");

    // Hit Effect Logic
    useEffect(() => {
        let type: BenchHit = "none";
        if (typeof integrityDelta === "number" && integrityDelta < 0) {
            type = "player";
        }
        if (typeof bossHpDelta === "number" && bossHpDelta < 0) {
            type = type === "player" ? "both" : "boss";
        }
        if (type === "none") return;

        setBenchHit(type);
        setActivityHit("tick");

        const t1 = setTimeout(() => setBenchHit("none"), 260);
        const t2 = setTimeout(() => setActivityHit("none"), 260);
        return () => {
            clearTimeout(t1);
            clearTimeout(t2);
        };
    }, [integrityDelta, bossHpDelta]);

    const benchHitClass =
        benchHit === "player"
            ? "ring-2 ring-rose-500/80 shadow-[0_0_32px_rgba(248,113,113,0.7)]"
            : benchHit === "boss"
                ? "ring-2 ring-emerald-400/80 shadow-[0_0_32px_rgba(52,211,153,0.7)]"
                : benchHit === "both"
                    ? "ring-2 ring-purple-400/80 shadow-[0_0_38px_rgba(168,85,247,0.8)]"
                    : "";

    // --- SHELL LOGIC ---

    // 1. Docked Rail Visibility
    // - Always visible in List View (!isWorkbench)
    // - NEVER visible in Quest View (isWorkbench) -> features moved to terminal tabs
    const showDockedRail = !isWorkbench;

    return (
        <main
            className="h-screen overflow-hidden flex flex-col text-workshop-text transition-colors duration-500 bg-workshop-bg font-sans selection:bg-workshop-violet/20"
            data-testid="layout-workshop"
        >
            {/* Ambient Background */}
            <div className="fixed inset-0 pointer-events-none transition-opacity duration-700">
                <div className="absolute top-0 left-0 w-full h-[500px] bg-workshop-cyan/5 blur-[120px]" />
                <div className="absolute bottom-0 right-0 w-full h-[500px] bg-workshop-violet/5 blur-[120px]" />
            </div>

            {/* Top HUD (Hidden in Quests) */}
            {!isWorkbench && (
                <header className="relative z-20 px-6 pt-4 pb-2 bg-workshop-bg/50 backdrop-blur-sm border-b border-white/5">
                    <div className="flex flex-wrap items-center justify-between gap-3">
                        {/* Left Group */}
                        <div className="flex flex-wrap items-center gap-3">
                            <div className="flex items-center gap-2">
                                <span className="text-xs font-semibold text-workshop-subtle tracking-wide uppercase">
                                    World
                                </span>
                                <div className="rounded-full bg-workshop-panel border border-white/10 shadow-workshop-neon overflow-hidden">
                                    {worldSelector}
                                </div>
                            </div>
                        </div>

                        {/* Right Group: Project + Extras */}
                        <div className="flex flex-wrap items-center gap-3">
                            {/* Project Badge - Contextual */}
                            <div className="hidden md:flex items-center gap-3">
                                {activeTrack ? (
                                    <div className="rounded-full bg-workshop-panel border border-white/10 px-4 py-1.5 text-xs font-medium text-workshop-text shadow-workshop-violet flex items-center gap-2">
                                        <span className="text-workshop-subtle">Project:</span>
                                        <span className="text-workshop-violet">{activeTrack.label || activeTrack.trackSlug}</span>
                                    </div>
                                ) : null}
                            </div>
                            {extraTopRight}

                            {/* Sprint 22.5: Supplementary page links */}
                            <div className="flex items-center gap-1">
                                <Link
                                    to="/arcade/codex"
                                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium text-workshop-subtle hover:text-workshop-cyan border border-transparent hover:border-workshop-cyan/20 hover:bg-workshop-cyan/5 transition-all"
                                    title="Codex — Knowledge Base"
                                >
                                    <BookOpen className="w-3.5 h-3.5" />
                                    <span className="hidden sm:inline">Codex</span>
                                </Link>
                                <Link
                                    to="/arcade/progress"
                                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium text-workshop-subtle hover:text-workshop-violet border border-transparent hover:border-workshop-violet/20 hover:bg-workshop-violet/5 transition-all"
                                    title="Progress — Quest Completion"
                                >
                                    <BarChart2 className="w-3.5 h-3.5" />
                                    <span className="hidden sm:inline">Progress</span>
                                </Link>
                            </div>

                            {/* Sprint 22.6: Map toggle removed — Board is the only world-selection view. */}
                        </div>
                    </div>
                </header>
            )}

            {/* Main Grid */}
            <section className="relative z-10 flex-1 px-6 pb-6 pt-2 overflow-hidden">
                <div
                    className={cn("grid h-full gap-6 grid-cols-1", showDockedRail ? "md:grid-cols-[2fr_1fr]" : "")}
                    data-rail-visible={showDockedRail}
                >

                    {/* LEFT COLUMN: Workbench */}
                    <section
                        className={cn("flex min-h-0 flex-1 flex-col", benchHitClass)}
                        data-testid="workshop-workbench"
                    >
                        <WorkbenchHeader onGuide={openWorkshopGuide} />

                        {/* scroll container */}
                        <div className="mt-3 flex-1 overflow-y-auto pr-1 pb-6 relative">
                            {/* Sprint 22.6: Always Board view — Map toggle removed. */}
                            {questPanel}
                        </div>
                    </section>

                    {/* RIGHT COLUMN: Docked Rail */}
                    {showDockedRail && (
                        <aside
                            className="hidden md:flex flex-col gap-3 h-full min-w-[320px] overflow-hidden"
                            data-testid="workshop-tools-panel"
                        >
                            {/* 1. Status Panel (Intent Oracle) */}
                            <section className="rounded-2xl border border-slate-800/70 bg-slate-950/70 p-3 shrink-0">
                                <div className="flex items-center justify-between border-b border-white/5 pb-2 mb-2">
                                    <div className="flex items-center gap-2">
                                        <EyeIcon className="w-4 h-4 text-workshop-violet" />
                                        <span className="text-xs font-bold text-slate-200">Intent Oracle</span>
                                    </div>
                                    <span className="text-[10px] text-emerald-400 font-mono">ONLINE</span>
                                </div>
                                {bossHud}
                            </section>

                            {/* 2. Content */}
                            {isWorkbench ? (
                                /* WORKBENCH MODE -> TOOLS PANEL */
                                <section className="flex-1 min-h-0 rounded-xl overflow-hidden shadow-workshop-panel">
                                    <WorkshopToolsPanel
                                        activePanel={activePanel}
                                        onPanelChange={handlePanelChange}
                                        resultsContent={
                                            <div className="space-y-4">
                                                {projectPanel}
                                            </div>
                                        }
                                        hasSkill={hasSkill}
                                        questSlug={params.questId}
                                        initialCodexTerm={activeCodexTerm}
                                    />
                                </section>
                            ) : (
                                /* LIST MODE -> GAUNTLET + INFO */
                                <div className="space-y-4 overflow-y-auto">
                                    {projectPanel}
                                    <PracticeGauntletCard />
                                </div>
                            )}
                        </aside>
                    )}

                </div>
            </section>

            {/* GLOBAL CODEX DRAWER */}
            <CodexDrawer
                isOpen={codexIsOpen}
                activeRef={activeCodexTerm || null}
                onClose={handleCodexClose}
                onOpenCodex={handleOpenCodex}
                questSlug={params.questId}
            />
        </main>
    );
};
