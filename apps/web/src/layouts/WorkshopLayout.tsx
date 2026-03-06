import React, { useEffect } from "react";
import { openWorkshopGuide } from "../features/workshop/useWorkshopTips";
import { PracticeGauntletCard } from "../components/practice/PracticeGauntletCard";
import { useParams, useSearchParams } from "react-router-dom";
import { useQuestStore, QuestState } from "../store/questStore";
import { useGameStore } from "../store/gameStore";
import { useCurrentLayout } from "../hooks/useCurrentLayout"; // Added import
import { cn } from "../lib/utils";
import { EyeIcon } from "lucide-react";
import { WorkshopToolsPanel } from "../components/workshop/WorkshopToolsPanel";
import { PanelId } from "../features/workshop/workshopPanels";
import { OrionMap } from "./OrionMap";

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
    // 1. Layout & Route Context
    const { layout } = useCurrentLayout();
    const params = useParams<{ worldSlug?: string; questId?: string; bossSlug?: string }>();
    const [searchParams, setSearchParams] = useSearchParams();

    // "Workbench" state = inside a quest. "List" state = board/index.
    const isWorkbench = Boolean(params.questId);
    const isCyberdeck = layout === 'cyberdeck';
    const isOrion = layout === 'orion';

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

    // 2. Orion Overlay Logic
    const [orionToolsOpen, setOrionToolsOpen] = React.useState(false);

    // DEBUG LOGGING (Moved to be valid)
    useEffect(() => {
        console.log('[WorkshopLayout Debug]', {
            layout,
            isWorkbench,
            isCyberdeck,
            isOrion,
            questId: params.questId,
            showDockedRail,
            orionToolsOpen
        });
    }, [layout, isWorkbench, params.questId, showDockedRail, orionToolsOpen]);

    // Close overlay when leaving Orion (prevents state leakage)
    useEffect(() => {
        if (!isOrion) {
            setOrionToolsOpen(false);
        }
    }, [isOrion]);

    // Ensure Orion overlay opens when deep linking to a tool
    useEffect(() => {
        if (isOrion && activePanel && ['judge', 'explain', 'debug', 'codex'].includes(activePanel)) {
            setOrionToolsOpen(true);
        }
    }, [isOrion, activePanel]);

    // Derived overlay visibility
    const showOrionOverlay = isWorkbench && isOrion && orionToolsOpen;

    return (
        <main
            className={cn(
                "h-screen overflow-hidden flex flex-col text-workshop-text transition-colors duration-500",
                isCyberdeck ? "bg-black font-mono selection:bg-cyan-900/50" : "bg-workshop-bg font-sans selection:bg-workshop-violet/20"
            )}
            data-testid="layout-workshop"
            data-layout={layout}
        >
            {/* Ambient Background */}
            <div className="fixed inset-0 pointer-events-none transition-opacity duration-700">
                {isOrion ? (
                    <>
                        <div className="absolute top-0 left-0 w-full h-[500px] bg-workshop-cyan/5 blur-[120px]" />
                        <div className="absolute bottom-0 right-0 w-full h-[500px] bg-workshop-violet/5 blur-[120px]" />
                        <div className="orion-starfield-layer opacity-40 mix-blend-screen" />
                    </>
                ) : (
                    /* Cyberdeck Background: Technical Grid */
                    <div className="absolute inset-0 bg-[linear-gradient(rgba(18,18,18,0)_2px,transparent_2px),linear-gradient(90deg,rgba(18,18,18,0)_2px,transparent_2px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_80%_80%_at_50%_50%,#000_40%,transparent_100%)] opacity-20" style={{ backgroundColor: '#050505' }}>
                        <div className="absolute inset-0 bg-cyan-950/5" />
                    </div>
                )}
            </div>

            {/* Top HUD */}
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

                        {/* Layout-Specific Header Controls (Orion Tools Toggle) */}
                        {isWorkbench && isOrion && (
                            <button
                                onClick={() => setOrionToolsOpen(true)}
                                data-testid="orion-tools-toggle"
                                className="px-3 py-1.5 rounded border border-cyan-500/30 bg-cyan-500/10 text-cyan-400 text-xs font-bold uppercase tracking-wider hover:bg-cyan-500/20"
                            >
                                Tools
                            </button>
                        )}
                    </div>
                </div>
            </header>

            {/* Main Grid */}
            <section className="relative z-10 flex-1 px-6 pb-6 pt-2 overflow-hidden">
                <div
                    key={layout} // Force remount on layout switch to re-calculate classes
                    className={cn("grid h-full gap-6 grid-cols-1", showDockedRail ? "md:grid-cols-[2fr_1fr]" : "")}
                    data-rail-visible={showDockedRail}
                    data-layout-state={layout}
                >

                    {/* LEFT COLUMN: Workbench */}
                    <section
                        className={cn("flex min-h-0 flex-1 flex-col", benchHitClass)}
                        data-testid="workshop-workbench"
                    >
                        <WorkbenchHeader onGuide={openWorkshopGuide} />

                        {/* scroll container */}
                        <div className="mt-3 flex-1 overflow-y-auto pr-1 pb-6 relative">
                            {/* LIST VIEW: Show Map (Orion) or Quest Panel (Standard) */}
                            {!isWorkbench && isOrion ? (
                                <div className="h-full w-full rounded-2xl overflow-hidden border border-cyan-500/20 shadow-2xl relative">
                                    <OrionMap />
                                </div>
                            ) : (
                                questPanel
                            )}
                        </div>
                    </section>

                    {/* RIGHT COLUMN: Docked Rail */}
                    {showDockedRail && (
                        <aside
                            key={layout} // Force remount on layout switch to prevent stale state
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

                    {/* ORION TOOLS OVERLAY */}
                    {showOrionOverlay && (
                        <div
                            className="absolute inset-y-0 right-0 w-[400px] z-50 bg-slate-950/95 border-l border-cyan-500/30 shadow-2xl backdrop-blur-xl flex flex-col p-4 animate-in slide-in-from-right duration-200"
                            data-testid="tools-overlay"
                        >
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="text-sm font-bold uppercase tracking-widest text-cyan-400">Workshop Tools</h3>
                                <button onClick={() => setOrionToolsOpen(false)} className="text-slate-400 hover:text-white">✕</button>
                            </div>
                            <div className="flex-1 overflow-hidden rounded-xl border border-white/10">
                                <WorkshopToolsPanel
                                    activePanel={activePanel}
                                    onPanelChange={handlePanelChange}
                                    resultsContent={
                                        <div className="space-y-4">
                                            {projectPanel}
                                        </div>
                                    }
                                    questSlug={params.questId}
                                    hasSkill={hasSkill}
                                    initialCodexTerm={activeCodexTerm}
                                />
                            </div>
                        </div>
                    )}
                </div>
            </section>
        </main>
    );
};
