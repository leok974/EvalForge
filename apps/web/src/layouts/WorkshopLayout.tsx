import React, { useEffect } from "react";
import { openWorkshopGuide } from "../features/workshop/useWorkshopTips";
import { PracticeGauntletCard } from "../components/practice/PracticeGauntletCard";
import { useParams, useSearchParams } from "react-router-dom";
import { useQuestStore, QuestState } from "../store/questStore";
import { useGameStore } from "../store/gameStore";
import { cn } from "../lib/utils";
import { EyeIcon } from "lucide-react";
import { WorkshopToolsPanel } from "../components/workshop/WorkshopToolsPanel";
import { PanelId } from "../features/workshop/workshopPanels";

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
    // DEBUG: Verify component reload
    useEffect(() => {
        console.log("🛠️ WorkshopLayout Refactored: Tools Panel Active");
    }, []);

    // Routing Integration
    const params = useParams<{ worldSlug?: string; questId?: string; bossSlug?: string }>();
    const [searchParams] = useSearchParams();

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

    // Local state for hit effects only
    const [benchHit, setBenchHit] = React.useState<BenchHit>("none");
    const [activityHit, setActivityHit] = React.useState<"none" | "tick">("none");

    // Whenever deltas change, trigger a short “flash” on the workbench.
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

    // Map currentMode to PanelId safely
    const activePanel: PanelId = (currentMode === 'quest' ? 'judge' : currentMode) as PanelId;

    return (
        <main
            className="h-screen bg-workshop-bg text-workshop-text overflow-hidden flex flex-col font-sans"
            data-testid="layout-workshop"
        >
            {/* Ambient Background */}
            <div className="fixed inset-0 pointer-events-none">
                <div className="absolute top-0 left-0 w-full h-[500px] bg-workshop-cyan/5 blur-[120px]" />
                <div className="absolute bottom-0 right-0 w-full h-[500px] bg-workshop-violet/5 blur-[120px]" />
                <div className="orion-starfield-layer opacity-40 mix-blend-screen" />
            </div>

            {/* Top HUD - Single Row Now */}
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
                        <div className="hidden md:flex items-center gap-3">
                            {activeTrack ? (
                                <div className="rounded-full bg-workshop-panel border border-white/10 px-4 py-1.5 text-xs font-medium text-workshop-text shadow-workshop-violet flex items-center gap-2">
                                    <span className="text-workshop-subtle">Project:</span>
                                    <span className="text-workshop-violet">{activeTrack.label || activeTrack.trackSlug}</span>
                                </div>
                            ) : (
                                <div className="rounded-full bg-workshop-panel border border-white/10 px-4 py-1.5 text-xs font-medium text-workshop-text shadow-workshop-violet flex items-center gap-2 opacity-50">
                                    <span className="text-workshop-subtle">Project:</span>
                                    <span className="italic">None Selected</span>
                                </div>
                            )}
                        </div>
                        {extraTopRight}
                    </div>
                </div>
                {/* Header Modes REMOVED */}
            </header>

            {/* Main Grid */}
            <section className="relative z-10 flex-1 px-6 pb-6 pt-2 overflow-hidden">
                <div className={cn("grid h-full gap-6 grid-cols-1", useQuestStore(s => s.focusMode) ? "" : "lg:grid-cols-[2fr_1fr]")}>

                    {/* LEFT COLUMN: Workbench – scrolls */}
                    <section
                        className={cn("flex min-h-0 flex-1 flex-col", benchHitClass)}
                        data-testid="workshop-workbench"
                    >
                        <WorkbenchHeader onGuide={openWorkshopGuide} />

                        {/* scroll container */}
                        <div className="mt-3 flex-1 overflow-y-auto pr-1 pb-6 relative">
                            {/* Quest Panel sits directly here */}
                            {questPanel}
                        </div>
                    </section>

                    {/* RIGHT COLUMN: Tools Panel */}
                    {!useQuestStore(s => s.focusMode) && (
                        <aside
                            className="hidden lg:flex flex-col gap-3 h-full min-w-[320px] overflow-hidden"
                            data-testid="workshop-tools-panel"
                        >
                            {/* 1. Status Panel (Intent Oracle) - Kept outside Tools Panel for visibility */}
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

                            {/* 2. Unified Tools Panel */}
                            <section className="flex-1 min-h-0 rounded-xl overflow-hidden shadow-workshop-panel">
                                <WorkshopToolsPanel
                                    activePanel={activePanel}
                                    onPanelChange={(p) => onModeChange?.(p)}
                                    // Mapping content to panels
                                    resultsContent={
                                        <div className="space-y-4">
                                            {projectPanel}
                                            <PracticeGauntletCard />
                                        </div>
                                    }
                                    codexContent={codexPanel}
                                    hasSkill={hasSkill}
                                />
                            </section>
                        </aside>
                    )}
                </div>
            </section>
        </main>
    );
};
