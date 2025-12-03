import * as React from "react";
import { cn } from "@/lib/utils";

type CyberdeckTopHudProps = {
    level: number;
    xp: number;
    xpToNext: number;
    systemIntegrity: number; // 0–100
    activeQuest: string;
    worldLabel: string;      // e.g. "PYTHON WORLD – APPLYLENS BACKEND"
    latencyMs: number | null;
    secure: boolean;
    online: boolean;
};

export function CyberdeckTopHud({
    level,
    xp,
    xpToNext,
    systemIntegrity,
    activeQuest,
    worldLabel,
    latencyMs,
    secure,
    online,
}: CyberdeckTopHudProps) {
    const pct =
        xpToNext > 0 ? Math.max(0, Math.min(100, (xp / xpToNext) * 100)) : 0;

    const integrityColor =
        systemIntegrity > 75
            ? "text-emerald-300"
            : systemIntegrity > 40
                ? "text-amber-300"
                : "text-rose-300";

    return (
        <header className="relative z-10 flex items-center justify-between border-b border-cyan-400/40 bg-[#020616]/95 px-5 py-3 shadow-[0_0_30px_rgba(56,189,248,0.3)]">
            {/* LEFT: Logo + integrity + XP */}
            <div className="flex items-center gap-4">
                {/* Logo / wordmark */}
                <div className="flex items-center gap-2">
                    <div className="h-7 w-7 rounded-xl bg-gradient-to-br from-cyan-400 to-fuchsia-500 shadow-[0_0_18px_rgba(244,114,182,0.7)]" />
                    <div className="flex flex-col leading-tight">
                        <span className="text-[11px] font-semibold tracking-[0.28em] text-slate-200">
                            EVALFORGE
                        </span>
                        <span className="text-[10px] font-medium tracking-[0.2em] text-slate-500">
                            CYBERDECK INTERFACE
                        </span>
                    </div>
                </div>

                {/* System integrity */}
                <div className="hidden items-center gap-2 md:flex">
                    <span className="text-[10px] font-semibold tracking-[0.24em] text-slate-400">
                        SYSTEM INTEGRITY
                    </span>
                    <span
                        className={cn(
                            "text-[11px] font-mono",
                            integrityColor
                        )}
                    >
                        {systemIntegrity.toFixed(0)}%
                    </span>
                </div>

                {/* XP + level */}
                <div className="hidden items-center gap-3 md:flex">
                    <div className="flex items-center gap-1">
                        <span className="text-[10px] font-semibold tracking-[0.24em] text-slate-400">
                            LEVEL
                        </span>
                        <span className="text-[12px] font-mono text-cyan-300">
                            {level}
                        </span>
                    </div>

                    <div className="flex min-w-[220px] flex-col gap-1">
                        <div className="flex items-center justify-between text-[9px] font-mono text-slate-400">
                            <span>XP</span>
                            <span>
                                {xp} / {xpToNext}
                            </span>
                        </div>
                        <div className="relative h-3 overflow-hidden rounded-full bg-slate-900/80">
                            {/* segmented background */}
                            <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(148,163,184,0.12)_1px,transparent_1px)] bg-[length:10px_100%]" />
                            {/* fill */}
                            <div
                                className="relative h-full w-0 bg-gradient-to-r from-cyan-400 via-sky-400 to-fuchsia-500 shadow-[0_0_20px_rgba(34,211,238,0.8)] transition-[width] duration-500 ease-out"
                                style={{ width: `${pct}%` }}
                            />
                        </div>
                    </div>
                </div>
            </div>

            {/* RIGHT: quest + status */}
            <div className="flex items-center gap-4">
                {/* Active quest */}
                <div className="hidden flex-col items-end md:flex">
                    <span className="text-[10px] font-semibold tracking-[0.24em] text-slate-500">
                        ACTIVE QUEST
                    </span>
                    <span className="max-w-[360px] truncate text-[11px] font-medium text-cyan-200">
                        {activeQuest || "NO QUEST SELECTED"}
                    </span>
                    <span className="max-w-[360px] truncate text-[9px] font-mono text-slate-500">
                        {worldLabel}
                    </span>
                </div>

                {/* Status pills */}
                <div className="flex items-center gap-2">
                    <HudPill
                        label={secure ? "SECURE" : "INSECURE"}
                        tone={secure ? "cyan" : "warn"}
                    />
                    <HudPill
                        label={online ? "ONLINE" : "OFFLINE"}
                        tone={online ? "green" : "warn"}
                    />
                    <HudPill
                        label={
                            latencyMs != null ? `${latencyMs.toFixed(0)}ms` : "--- ms"
                        }
                        tone="neutral"
                    />
                </div>
            </div>
        </header>
    );
}

type HudPillTone = "cyan" | "green" | "warn" | "neutral";

function HudPill({
    label,
    tone,
}: {
    label: string;
    tone: HudPillTone;
}) {
    const base =
        "inline-flex items-center rounded-full border px-3 py-1 text-[10px] font-semibold tracking-[0.22em] font-hud";

    const toneClass =
        tone === "cyan"
            ? "border-cyan-400/70 bg-cyan-500/10 text-cyan-200 shadow-[0_0_14px_rgba(34,211,238,0.55)]"
            : tone === "green"
                ? "border-emerald-400/70 bg-emerald-500/10 text-emerald-200 shadow-[0_0_14px_rgba(52,211,153,0.55)]"
                : tone === "warn"
                    ? "border-rose-400/80 bg-rose-500/10 text-rose-200 shadow-[0_0_16px_rgba(248,113,113,0.7)]"
                    : "border-slate-500/60 bg-slate-900/80 text-slate-200";

    return <span className={cn(base, toneClass)}>{label}</span>;
}
