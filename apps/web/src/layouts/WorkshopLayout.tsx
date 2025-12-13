import React, { useEffect, useState } from "react";
import { openWorkshopGuide } from "../features/workshop/useWorkshopTips";
import { PracticeGauntletCard } from "../components/practice/PracticeGauntletCard";
import { useParams, useSearchParams } from "react-router-dom";
import { useQuestStore, QuestState } from "../store/questStore";
import { NeonPanel } from "../components/workshop/NeonPanel";
import { cn } from "../lib/utils";
import { EyeIcon } from "lucide-react";

export type WorkshopMode = 'judge' | 'quest' | 'explain' | 'debug' | 'codex';

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

    // Mode Control
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
    currentMode = 'quest',
    onModeChange,
    hasSkill,
}) => {
    // Routing Integration
    const params = useParams<{ worldSlug?: string; questId?: string; bossSlug?: string }>();
    const [searchParams] = useSearchParams();

    // Store Actions
    const setActiveWorld = useQuestStore((s: QuestState) => s.setActiveWorldSlug);
    const setActiveTrack = useQuestStore((s: QuestState) => s.setActiveTrackId);
    const setActiveBoss = useQuestStore((s: QuestState) => s.setActiveBossSlug);

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

    const activityHitClass =
        activityHit === "tick"
            ? "ring-1 ring-emerald-300/70 shadow-[0_0_20px_rgba(52,211,153,0.6)]"
            : "";

    return (
        <main
            className="min-h-screen bg-workshop-bg text-workshop-text overflow-x-hidden flex flex-col font-sans"
            data-testid="layout-workshop"
        >
            {/* Ambient Background */}
            <div className="fixed inset-0 pointer-events-none">
                <div className="absolute top-0 left-0 w-full h-[500px] bg-workshop-cyan/5 blur-[120px]" />
                <div className="absolute bottom-0 right-0 w-full h-[500px] bg-workshop-violet/5 blur-[120px]" />
                <div className="orion-starfield-layer opacity-40 mix-blend-screen" />
            </div>

            {/* Top HUD - Two-row Layout */}
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
                            <div className="rounded-full bg-workshop-panel border border-white/10 px-4 py-1.5 text-xs font-medium text-workshop-text shadow-workshop-violet flex items-center gap-2">
                                <span className="text-workshop-subtle">Project:</span>
                                <span className="text-workshop-violet">ApplyLens – Backend</span>
                            </div>
                        </div>
                        {extraTopRight}
                    </div>
                </div>

                {/* Second Row: Mode Tabs */}
                <div className="mt-3 flex flex-wrap gap-2 pb-2">
                    <nav className="inline-flex flex-wrap gap-1 rounded-full bg-slate-900/80 p-1">
                        {['JUDGE', 'QUEST', 'EXPLAIN', 'DEBUG', 'CODEX'].map((tab) => {
                            const tabKey = tab.toLowerCase();
                            const isActive = currentMode === tabKey;
                            // Determine lock status based on skill
                            let isLocked = false;
                            if (tabKey === 'explain' && hasSkill && !hasSkill('agent_explain')) isLocked = true;
                            if (tabKey === 'debug' && hasSkill && !hasSkill('agent_debug')) isLocked = true;

                            return (
                                <button
                                    key={tab}
                                    type="button"
                                    disabled={isLocked}
                                    className={cn(
                                        'relative px-4 py-1.5 text-[10px] font-bold tracking-widest rounded-full transition-all duration-200 flex items-center gap-1',
                                        isActive
                                            ? 'bg-workshop-panel border border-workshop-cyan/80 text-workshop-cyan shadow-workshop-neon'
                                            : isLocked
                                                ? 'bg-transparent border border-transparent text-workshop-subtle/50 cursor-not-allowed'
                                                : 'bg-transparent border border-white/5 text-workshop-subtle hover:border-workshop-cyan/40 hover:text-workshop-text'
                                    )}
                                    onClick={() => !isLocked && onModeChange?.(tabKey as WorkshopMode)}
                                >
                                    {tab} {isLocked && '🔒'}
                                </button>
                            );
                        })}
                    </nav>
                </div>
            </header>

            {/* Main Grid */}
            <section className="relative z-10 flex-1 px-6 pb-6 pt-2 overflow-hidden">
                <div className="grid h-full gap-6 grid-cols-1 lg:grid-cols-[2fr_1fr]">

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

                        {/* Activity Feed at bottom of column? Or separate? 
                            User snippet didn't explicitly show activity feed. 
                            I'll keep it as a small section below or integrated.
                            The previous code had it in a NeonPanel at bottom.
                            I'll put it in a small card at the bottom.
                        */}
                        <div className={cn("mt-4 h-32 shrink-0 rounded-2xl border border-slate-800/70 bg-slate-950/60 p-0 overflow-hidden", activityHitClass)} data-testid="workshop-activity-strip">
                            <div className="w-full h-full overflow-auto bg-black/20 p-2">
                                {activityFeed}
                            </div>
                        </div>
                    </section>

                    {/* RIGHT COLUMN: Project Bench + Practice – fixed */}
                    <aside
                        className="hidden lg:flex flex-col gap-3 h-full min-w-[320px] overflow-y-auto pr-1 pb-2 scrollbar-thin scrollbar-thumb-workshop-subtle/20"
                        data-testid="workshop-project-bench"
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
                            {/* Boss HUD (mini) or Status checks */}
                            {bossHud}
                        </section>

                        {/* 2. Project Panel Content (Judge/Scoreboard) */}
                        <section className="rounded-2xl border border-slate-800/70 bg-slate-950/70 p-3 shrink-0">
                            {projectPanel}
                        </section>

                        {/* 3. Assignments (Practice Gauntlet) */}
                        <section className="flex min-h-0 flex-1 flex-col rounded-2xl border border-slate-800/70 bg-slate-950/70 p-3">
                            {/* Header provided by PracticeGauntletCard or here? User snippet for AssignmentsPanel had header INSIDE.
                                 But PracticeGauntletCard has its own header.
                                 I'll let PracticeGauntletCard handle the layout inside this flex container.
                                 I need to make sure PracticeGauntletCard takes full height as well.
                             */}
                            <PracticeGauntletCard />
                        </section>

                        {/* 4. Codex Shelf (if needed) */}
                        <section className="rounded-2xl border border-slate-800/70 bg-slate-950/70 p-3 shrink-0 min-h-[100px]" data-testid="workshop-codex-shelf">
                            <div className="text-[10px] uppercase tracking-wider text-workshop-subtle mb-2">Codex Shelf</div>
                            <div className="max-h-32 overflow-auto">
                                {codexPanel}
                            </div>
                        </section>
                    </aside>
                </div>
            </section>
        </main>
    );
};
