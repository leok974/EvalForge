import { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function DeckPanel({ children, title, className }: { children: ReactNode; title?: string; className?: string }) {
    return (
        <div className={cn("relative overflow-hidden rounded-2xl border border-cyan-400/30 bg-gradient-to-b from-slate-900/70 via-slate-950/90 to-slate-950/95 shadow-[0_0_24px_rgba(0,255,255,0.16)]", className)}>
            {title && (
                <div className="border-b border-cyan-400/20 bg-slate-900/50 px-3 py-2 text-[10px] font-hud tracking-[0.25em] text-cyan-200">
                    {title.toUpperCase()}
                </div>
            )}
            <div className="p-3 text-xs h-full">{children}</div>
            {/* subtle scanline/gradient overlay */}
            <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,#3b82f6/18,transparent_55%),linear-gradient(to_bottom,rgba(148,163,184,0.12),transparent)] mix-blend-screen opacity-60" />
        </div>
    );
}
