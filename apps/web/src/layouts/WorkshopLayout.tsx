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
            className="min-h-screen bg-workshop-bg text-workshop-text overflow-hidden flex flex-col font-sans"
            data-testid="layout-workshop"
        >
            {/* Ambient Background */}
            <div className="fixed inset-0 pointer-events-none">
                <div className="absolute top-0 left-0 w-full h-[500px] bg-workshop-cyan/5 blur-[120px]" />
                <div className="absolute bottom-0 right-0 w-full h-[500px] bg-workshop-violet/5 blur-[120px]" />
                <div className="orion-starfield-layer opacity-40 mix-blend-screen" />
            </div>

            {/* Top HUD */}
            <header className="relative z-20 px-6 pt-5 pb-4 flex items-center justify-between gap-6 bg-workshop-bg/50 backdrop-blur-sm border-b border-white/5">
                <div className="flex items-center gap-6">
                    <div className="flex items-center gap-3">
                        <span className="text-sm font-semibold text-workshop-subtle tracking-wide uppercase">
                            World Selector
                        </span>
                        {/* Wrapper for existing component with Neon styling override if needed */}
                        <div className="rounded-full bg-workshop-panel border border-white/10 shadow-workshop-neon overflow-hidden">
                            {worldSelector}
                        </div>
                    </div>

                    <div className="hidden md:flex items-center gap-3">
                        {/* Project Placeholder - or actual component if available */}
                        <div className="rounded-full bg-workshop-panel border border-white/10 px-4 py-1.5 text-xs font-medium text-workshop-text shadow-workshop-violet flex items-center gap-2">
                            <span className="text-workshop-subtle">Project:</span>
                            <span className="text-workshop-violet">ApplyLens – Backend</span>
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-2">
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
                                    'relative px-5 py-2 text-[10px] font-bold tracking-widest rounded-full transition-all duration-200 flex items-center gap-1',
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
                </div>

                {extraTopRight && <div className="ml-4">{extraTopRight}</div>}
            </header>

            {/* Main Grid */}
            <section className="relative z-10 flex-1 px-6 pb-6 pt-6 overflow-hidden">
                <div className="grid h-full gap-6 grid-cols-1 lg:grid-cols-[2fr_1fr]">

                    {/* LEFT COLUMN: Workbench */}
                    <div
                        className={cn("flex flex-col gap-4 min-h-0", benchHitClass)}
                        data-testid="workshop-workbench"
                    >
                        <div className="flex items-center justify-between text-xs font-semibold tracking-[0.2em] text-workshop-subtle uppercase px-1">
                            <span>Workbench</span>
                            <button onClick={openWorkshopGuide} className="hover:text-workshop-cyan transition-colors">
                                ? Help
                            </button>
                        </div>

                        {/* Code Editor Panel */}
                        <NeonPanel className="flex-1 flex flex-col overflow-hidden p-0 bg-workshop-panel/95">
                            {/* Quest Panel fills this space */}
                            <div className="w-full h-full relative">
                                {questPanel}
                            </div>
                        </NeonPanel>

                        {/* Log/Activity Panel */}
                        <NeonPanel
                            variant="subtle"
                            className={cn("h-48 flex flex-col overflow-hidden p-0", activityHitClass)}
                            data-testid="workshop-activity-strip"
                        >
                            <div className="w-full h-full overflow-auto bg-black/40">
                                {activityFeed}
                            </div>
                        </NeonPanel>
                    </div>

                    {/* RIGHT COLUMN: Project Bench + Practice */}
                    <aside
                        className="flex flex-col gap-4 min-h-0 overflow-y-auto pr-1 pb-2 scrollbar-thin scrollbar-thumb-workshop-subtle/20"
                        data-testid="workshop-project-bench"
                    >
                        <div className="text-xs font-semibold tracking-[0.2em] text-workshop-subtle uppercase px-1">
                            Project Bench
                        </div>

                        {/* Intent Oracle Status Card & Project Controls */}
                        <NeonPanel variant="violet" className="p-5 flex flex-col gap-3 shrink-0">
                            <div className="flex items-center justify-between border-b border-workshop-violet/20 pb-3">
                                <div className="flex items-center gap-3">
                                    <div className="p-2 rounded-lg bg-workshop-violet/10 ring-1 ring-workshop-violet/40">
                                        <EyeIcon className="w-5 h-5 text-workshop-violet" />
                                    </div>
                                    <div>
                                        <div className="font-bold text-sm text-workshop-text">Intent Oracle</div>
                                        <div className="text-[10px] text-workshop-subtle uppercase tracking-wider">Automated Judge</div>
                                    </div>
                                </div>
                                <div className="flex items-center gap-1.5">
                                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse shadow-[0_0_8px_rgba(52,211,153,0.8)]" />
                                </div>
                            </div>

                            <div className="text-xs flex items-center justify-between text-workshop-subtle/80 font-mono">
                                <span>Status: <span className="text-emerald-400">Online</span></span>
                                <span>Latency: <span className="text-workshop-cyan">12ms</span></span>
                            </div>

                            {/* Render actual Boss HUD here if needed, or keeping it separate */}
                            {bossHud}

                            {/* We also render projectPanel to ensure functionality (Scoreboard, Eval buttons etc) are present 
                                even if visual duplication occurs with Top tabs. 
                            */}
                            <div className="mt-2 border-t border-white/5 pt-2">
                                {projectPanel}
                            </div>
                        </NeonPanel>

                        {/* Practice Gauntlet */}
                        <div className="text-xs font-semibold tracking-[0.2em] text-workshop-subtle uppercase px-1 mt-2">
                            Assignments
                        </div>
                        <PracticeGauntletCard />

                        {/* Codex Shelf (optional if space permits, or hide) */}
                        <div className="mt-auto pt-4" data-testid="workshop-codex-shelf">
                            <NeonPanel variant="subtle" className="p-4 min-h-[100px]">
                                <div className="text-[10px] uppercase tracking-wider text-workshop-subtle mb-2">Codex Shelf</div>
                                <div className="max-h-32 overflow-auto">
                                    {codexPanel}
                                </div>
                            </NeonPanel>
                        </div>
                    </aside>
                </div>
            </section>
        </main>
    );
};
