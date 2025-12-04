import React from "react";

type StepStatus = "locked" | "available" | "completed";

export interface OracleTrackState {
    invocation: StepStatus;
    grounding: StepStatus;
    boss: StepStatus;
}

interface OracleTrackCardProps {
    state: OracleTrackState;
    onOpenTrack?: () => void;
    onOpenBossCodex?: () => void;
}

const statusLabel: Record<StepStatus, string> = {
    locked: "Locked",
    available: "Available",
    completed: "Completed",
};

const statusBadgeClasses: Record<StepStatus, string> = {
    locked:
        "border border-cyan-700/50 text-cyan-500/40 bg-cyan-900/10",
    available:
        "border border-emerald-400/70 text-emerald-300 bg-emerald-500/10",
    completed:
        "border border-amber-400/70 text-amber-200 bg-amber-500/10",
};

const dotClasses: Record<StepStatus, string> = {
    locked: "bg-cyan-500/25",
    available: "bg-emerald-400",
    completed: "bg-amber-300",
};

export const OracleTrackCard: React.FC<OracleTrackCardProps> = ({
    state,
    onOpenTrack,
    onOpenBossCodex,
}) => {
    const steps = [
        {
            id: "invocation",
            title: "Invocation",
            subtitle: "Basic planner with allowed tools only",
            status: state.invocation,
        },
        {
            id: "grounding",
            title: "Grounding",
            subtitle: "Safety, constraints & refusals",
            status: state.grounding,
        },
        {
            id: "boss",
            title: "Boss: The Intent Oracle",
            subtitle: "Full planner eval with Codex hints",
            status: state.boss,
        },
    ] as const;

    return (
        <div
            className={`
        relative overflow-hidden rounded-2xl border border-cyan-500/40
        bg-gradient-to-br from-slate-950/90 via-slate-950/60 to-cyan-900/30
        shadow-[0_0_40px_rgba(0,255,255,0.18)] px-4 py-3 sm:px-5 sm:py-4
      `}
            data-testid="oracle-track-card"
        >
            {/* subtle grid + glow background */}
            <div className="pointer-events-none absolute inset-0 opacity-20">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(56,189,248,0.25),transparent_60%)]" />
                <div className="absolute inset-0 bg-[linear-gradient(90deg,rgba(148,163,184,0.10)_1px,transparent_1px),linear-gradient(180deg,rgba(148,163,184,0.10)_1px,transparent_1px)] bg-[size:26px_26px]" />
            </div>

            {/* Header row */}
            <div className="relative flex items-start justify-between gap-3">
                <div>
                    <div className="inline-flex items-center gap-2 rounded-full border border-cyan-500/40 bg-slate-950/70 px-3 py-1 text-xs font-medium tracking-wide text-cyan-200">
                        <span className="h-1.5 w-1.5 rounded-full bg-cyan-300 shadow-[0_0_8px_rgba(34,211,238,0.9)]" />
                        THE ORACLE • AGENT TRACK
                    </div>
                    <h3 className="mt-2 text-base font-semibold tracking-tight text-slate-50">
                        Invocation &amp; Grounding
                    </h3>
                    <p className="mt-1 text-xs sm:text-[13px] text-slate-300/80">
                        Learn to turn messy human goals into safe, structured plans before
                        facing <span className="text-cyan-200">The Intent Oracle</span>.
                    </p>
                </div>

                {/* Boss banner mini-badge */}
                <div className="flex flex-col items-end gap-1 text-right">
                    <div className="inline-flex items-center gap-1.5 rounded-full border border-fuchsia-400/70 bg-fuchsia-900/20 px-2.5 py-1 text-[11px] uppercase tracking-[0.12em] text-fuchsia-100">
                        <span className="h-1.5 w-1.5 rounded-full bg-fuchsia-300 animate-pulse" />
                        Boss Ready
                    </div>
                    <div className="rounded-xl bg-slate-950/70 px-2 py-1 text-[10px] text-slate-300/80 border border-slate-600/60">
                        World: <span className="text-cyan-200">The Oracle</span>
                    </div>
                </div>
            </div>

            {/* Steps */}
            <div className="relative mt-3 grid gap-2.5">
                {steps.map((step, idx) => (
                    <div
                        key={step.id}
                        className={`
              flex items-center justify-between gap-3 rounded-xl border
              bg-slate-950/60 px-2.5 py-2 sm:px-3 sm:py-2.5
              ${step.id === "boss"
                                ? "border-fuchsia-500/60"
                                : "border-cyan-500/35"
                            }
            `}
                    >
                        <div className="flex items-center gap-2.5">
                            {/* step dot + index */}
                            <div className="flex h-7 w-7 items-center justify-center rounded-full bg-slate-900/90 border border-slate-600/80">
                                <span
                                    className={`h-2 w-2 rounded-full ${dotClasses[step.status]} shadow-[0_0_12px_rgba(34,211,238,0.6)]`}
                                />
                            </div>
                            <div>
                                <div className="flex items-center gap-2">
                                    <span className="text-sm font-medium text-slate-50">
                                        {idx + 1}. {step.title}
                                    </span>
                                    {step.id === "boss" && (
                                        <span className="rounded-full border border-fuchsia-400/70 bg-fuchsia-500/10 px-2 py-[1px] text-[10px] font-semibold uppercase tracking-[0.14em] text-fuchsia-200">
                                            Boss
                                        </span>
                                    )}
                                </div>
                                <p className="text-[11px] text-slate-300/80">
                                    {step.subtitle}
                                </p>
                            </div>
                        </div>
                        <div
                            className={`
                inline-flex items-center gap-1.5 rounded-full px-2.5 py-1
                text-[11px] font-medium
                ${statusBadgeClasses[step.status]}
              `}
                        >
                            <span className="h-1.5 w-1.5 rounded-full bg-current" />
                            <span>{statusLabel[step.status]}</span>
                        </div>
                    </div>
                ))}
            </div>

            {/* Footer actions */}
            <div className="relative mt-3 flex flex-wrap items-center justify-between gap-2">
                <div className="text-[11px] text-slate-400">
                    Boss hint codex:{" "}
                    <button
                        type="button"
                        className="underline decoration-dotted decoration-cyan-400/80 underline-offset-2 hover:text-cyan-200"
                        onClick={onOpenBossCodex}
                        data-testid="oracle-track-open-codex"
                    >
                        Intent Oracle Strategy
                    </button>
                </div>

                <button
                    type="button"
                    onClick={onOpenTrack}
                    className={`
            inline-flex items-center gap-1.5 rounded-full border border-cyan-400/80
            bg-cyan-500/15 px-3 py-1.5 text-[11px] font-semibold uppercase
            tracking-[0.14em] text-cyan-100 hover:bg-cyan-500/25
          `}
                    data-testid="oracle-track-continue"
                >
                    <span className="h-1.5 w-1.5 rounded-full bg-cyan-300 animate-pulse" />
                    Continue track
                </button>
            </div>
        </div>
    );
};
