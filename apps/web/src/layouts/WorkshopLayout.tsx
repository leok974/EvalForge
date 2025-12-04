import React, { useEffect, useState } from "react";
import { openWorkshopGuide } from "../features/workshop/useWorkshopTips";
import { PracticeGauntletCard } from "../components/practice/PracticeGauntletCard";

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
}) => {
    const [benchHit, setBenchHit] = useState<BenchHit>("none");
    const [activityHit, setActivityHit] = useState<"none" | "tick">("none");

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
        <div
            className={`
        relative grid h-full w-full
        grid-rows-[auto,1fr,auto]
        bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950
        text-slate-100
        overflow-hidden
      `}
            data-testid="layout-workshop"
        >
            {/* Ambient background / floor */}
            <div
                aria-hidden="true"
                className="pointer-events-none absolute inset-0 opacity-60 mix-blend-screen"
            >
                <div className="absolute -left-24 top-10 h-64 w-64 rotate-[-8deg] rounded-[40%] bg-cyan-500/10 blur-3xl" />
                <div className="absolute -right-20 bottom-0 h-64 w-64 rotate-3 rounded-[40%] bg-amber-500/10 blur-3xl" />
                <div className="absolute inset-x-0 bottom-0 h-[45%] bg-[radial-gradient(circle_at_50%_0%,rgba(15,23,42,0)_0,rgba(15,23,42,0.8)_60%,rgba(15,23,42,1)_100%)]" />
            </div>

            {/* Top row: Boss + World selector + extra */}
            <header className="relative z-10 flex items-start justify-between gap-3 px-3 pt-3 sm:px-4 sm:pt-4">
                <div className="flex flex-1 flex-wrap items-start gap-3">
                    <div
                        className={`
              rounded-2xl border border-rose-500/60 bg-slate-950/90
              px-2.5 py-2 shadow-[0_18px_40px_rgba(248,113,113,0.45)]
              backdrop-blur-xl
              transform -rotate-1 hover:rotate-0 transition-transform duration-150
            `}
                    >
                        {bossHud}
                    </div>

                    <div
                        className={`
              rounded-2xl border border-cyan-500/60 bg-slate-950/90
              px-2.5 py-2 shadow-[0_18px_34px_rgba(34,211,238,0.4)]
              backdrop-blur-xl
              transform rotate-1 hover:rotate-0 transition-transform duration-150
            `}
                    >
                        {worldSelector}
                    </div>
                </div>

                {extraTopRight && (
                    <div className="hidden sm:block">
                        {extraTopRight}
                    </div>
                )}
            </header>

            {/* Middle row: Workbench + side benches */}
            <main
                className={`
          relative z-10 grid grid-cols-1 gap-4
          px-3 pb-3 pt-2 sm:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)] sm:px-4 sm:pb-4
        `}
            >
                {/* Center Workbench */}
                <section
                    className={`
            relative flex h-full flex-col
            rounded-[26px] border border-slate-700/80
            bg-slate-950/95
            shadow-[0_28px_60px_rgba(15,23,42,0.9)]
            overflow-hidden
            transform -rotate-[1.5deg] skew-y-[0.5deg]
            hover:rotate-[-0.5deg] hover:skew-y-0
            transition-transform duration-200
            ${benchHitClass}
          `}
                    data-testid="workshop-workbench"
                >
                    {/* Micro-animation: desk lamp glow */}
                    <div
                        aria-hidden="true"
                        className="pointer-events-none absolute -top-4 right-8 h-10 w-10 rounded-full bg-amber-400/70 blur-[8px] opacity-70 animate-pulse"
                    />
                    <div
                        aria-hidden="true"
                        className="pointer-events-none absolute -top-6 right-6 h-12 w-12 rounded-full border border-amber-300/40 opacity-40 animate-ping"
                    />

                    {/* “desk edge” */}
                    <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-slate-400/50 via-slate-100/70 to-slate-400/50 opacity-60" />
                    <div className="absolute inset-x-0 bottom-0 h-1 bg-gradient-to-r from-slate-700 via-slate-800 to-slate-900" />

                    <div className="flex items-center justify-between border-b border-slate-700/70 px-3 py-2">
                        <div className="flex items-center gap-1.5">
                            <span className="text-[11px] font-semibold uppercase tracking-[0.16em] text-slate-300">
                                Workbench
                            </span>
                        </div>
                        <div className="flex items-center gap-1.5">
                            <span className="hidden text-[10px] text-slate-500 sm:inline">
                                Quests • Boss Coding • Trials
                            </span>
                            <button
                                type="button"
                                onClick={openWorkshopGuide}
                                aria-label="Show Workshop help"
                                data-testid="workshop-guide-trigger"
                                className={`
                  inline-flex h-5 w-5 items-center justify-center
                  rounded-full border border-slate-600/80
                  bg-slate-900/80 text-[10px] font-semibold text-slate-200
                  hover:border-indigo-400 hover:text-indigo-200
                  transition-colors
                `}
                            >
                                ?
                            </button>
                        </div>
                    </div>

                    <div className="flex-1 overflow-hidden px-3 pb-3 pt-2 sm:px-4 sm:pb-4">
                        {questPanel}
                    </div>
                </section>

                {/* Right side: Project Bench + Codex Shelf */}
                <section
                    className={`
            flex h-full flex-col gap-3
            transform rotate-[1.2deg] skew-y-[-0.4deg]
            sm:pt-1
            transition-transform duration-200
            hover:rotate-[0.5deg] hover:skew-y-0
          `}
                >
                    {/* Project Bench */}
                    <div
                        className={`
              rounded-[22px] border border-emerald-500/60
              bg-slate-950/95
              shadow-[0_20px_40px_rgba(16,185,129,0.4)]
              backdrop-blur-xl
              overflow-hidden
            `}
                        data-testid="workshop-project-bench"
                    >
                        <div className="flex items-center justify-between border-b border-emerald-500/40 px-3 py-2">
                            <span className="text-[11px] font-semibold uppercase tracking-[0.16em] text-emerald-200">
                                Project Bench
                            </span>
                            <span className="text-[10px] text-emerald-100/80">
                                Synced Repos • ApplyLens • SiteAgent
                            </span>
                        </div>
                        <div className="max-h-[52vh] overflow-auto px-3 pb-3 pt-2 sm:px-4 sm:pb-4">
                            {projectPanel}
                        </div>
                    </div>

                    {/* Practice Gauntlet */}
                    <PracticeGauntletCard />

                    {/* Codex Shelf */}
                    <div
                        className={`
              rounded-[22px] border border-indigo-500/60
              bg-slate-950/95
              shadow-[0_18px_38px_rgba(129,140,248,0.45)]
              backdrop-blur-xl
              overflow-hidden
            `}
                        data-testid="workshop-codex-shelf"
                    >
                        <div className="flex items-center justify-between border-b border-indigo-500/40 px-3 py-2">
                            <span className="text-[11px] font-semibold uppercase tracking-[0.16em] text-indigo-200">
                                Codex Shelf
                            </span>
                            <span className="text-[10px] text-indigo-100/80">
                                Boss Guides • Project Docs
                            </span>
                        </div>
                        <div className="max-h-[32vh] overflow-auto px-3 pb-3 pt-2 sm:px-4 sm:pb-4">
                            {codexPanel}
                        </div>
                    </div>
                </section>
            </main>

            {/* Bottom row: activity strip */}
            <footer
                className={`
          relative z-10 flex items-stretch gap-3
          border-t border-slate-800/80
          bg-slate-950/95/60
          px-3 pb-2.5 pt-2 sm:px-4
        `}
            >
                <div
                    className={`
            relative flex-1 rounded-2xl border border-slate-700/80
            bg-slate-950/95
            shadow-[0_12px_26px_rgba(15,23,42,0.85)]
            backdrop-blur-xl
            overflow-hidden
            ${activityHitClass}
          `}
                    data-testid="workshop-activity-strip"
                >
                    {/* impact ripple overlay */}
                    {activityHit === "tick" && (
                        <div
                            aria-hidden="true"
                            className="pointer-events-none absolute inset-x-4 bottom-0 h-6 bg-gradient-to-t from-emerald-400/30 via-emerald-300/10 to-transparent animate-pulse"
                        />
                    )}

                    <div className="flex items-center justify-between border-b border-slate-800 px-3 py-1.5">
                        <span className="text-[10px] uppercase tracking-[0.16em] text-slate-400">
                            Activity Feed
                        </span>
                        <span className="text-[10px] text-slate-500">
                            Events • XP • Logs
                        </span>
                    </div>
                    <div className="max-h-32 overflow-auto px-3 pb-2 pt-1.5 sm:max-h-40 sm:px-4">
                        {activityFeed}
                    </div>
                </div>
            </footer>
        </div>
    );
};
