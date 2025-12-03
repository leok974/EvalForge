import React from "react";
import { fxEnabled } from "@/lib/featureFlags";
import { cn } from "@/lib/utils";

export function TerminalFrame({ children }: { children: React.ReactNode }) {
    return (
        <div
            className={cn(
                "relative h-full w-full rounded-2xl border border-cyan-400/40 bg-slate-950/90 shadow-[0_0_24px_rgba(34,211,238,0.35)]",
                "overflow-hidden"
            )}
        >
            {/* inner bezel */}
            <div className="absolute inset-[1px] rounded-[14px] bg-gradient-to-b from-slate-900/80 via-slate-950 to-black/95" />

            {/* content */}
            <div className="relative z-10 h-full w-full">
                {children}
            </div>

            {fxEnabled && (
                <>
                    {/* scanlines */}
                    <div className="pointer-events-none absolute inset-0 opacity-[0.13] mix-blend-soft-light scanline-animation" />

                    {/* subtle glow at top */}
                    <div className="pointer-events-none absolute inset-x-0 top-0 h-24 bg-gradient-to-b from-cyan-400/18 via-sky-400/6 to-transparent" />
                </>
            )}
        </div>
    );
}
