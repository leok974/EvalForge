import React, { useEffect } from "react";
import {
    useWorkshopTips,
    WORKSHOP_GUIDE_OPEN_EVENT,
} from "./useWorkshopTips";

interface WorkshopGuideProps {
    className?: string;
}

export const WorkshopGuide: React.FC<WorkshopGuideProps> = ({ className }) => {
    const { showTips, dismiss, open } = useWorkshopTips();

    // 🔹 Listen for global “open guide” event
    useEffect(() => {
        if (typeof window === "undefined") return;

        const handler = () => {
            open();
        };

        window.addEventListener(WORKSHOP_GUIDE_OPEN_EVENT, handler);
        return () => window.removeEventListener(WORKSHOP_GUIDE_OPEN_EVENT, handler);
    }, [open]);

    if (!showTips) return null;

    return (
        <div
            className={`
        rounded-2xl border border-indigo-400/70
        bg-slate-950/95 text-slate-100
        px-3 py-2.5 text-[11px]
        shadow-[0_18px_40px_rgba(129,140,248,0.4)]
        backdrop-blur-xl
        ${className ?? ""}
      `}
            data-testid="workshop-guide"
        >
            <div className="mb-1 flex items-center justify-between gap-2">
                <div className="flex items-center gap-1.5">
                    <span className="inline-flex h-1.5 w-1.5 rounded-full bg-indigo-300 shadow-[0_0_12px_rgba(129,140,248,0.9)]" />
                    <span className="text-[10px] font-semibold uppercase tracking-[0.16em] text-indigo-100">
                        Workshop Primer
                    </span>
                </div>
                <button
                    type="button"
                    onClick={dismiss}
                    className="rounded-full border border-slate-600/80 bg-slate-900/70 px-2 py-[1px] text-[9px] uppercase tracking-[0.16em] text-slate-300 hover:border-slate-400 hover:bg-slate-800/80"
                >
                    Got it
                </button>
            </div>

            <p className="mb-2 text-[11px] text-slate-200/90">
                The Workshop is your isometric lab where bosses, projects, and codex all
                meet. Think of it as your &quot;engineering desk&quot; inside EvalForge.
            </p>

            <ul className="space-y-1.5 text-[10px] text-slate-300">
                <li>
                    <span className="font-semibold text-emerald-200">Workbench</span>
                    <span className="text-slate-400"> —</span>{" "}
                    Run quests, boss coding trials, and high-stakes experiments here.
                </li>
                <li>
                    <span className="font-semibold text-emerald-200">Project Bench</span>
                    <span className="text-slate-400"> —</span>{" "}
                    View synced repos like{" "}
                    <span className="font-medium text-slate-100">ApplyLens</span>{" "}
                    or <span className="font-medium text-slate-100">SiteAgent</span> and
                    their status.
                </li>
                <li>
                    <span className="font-semibold text-emerald-200">Codex Shelf</span>
                    <span className="text-slate-400"> —</span>{" "}
                    Boss guides, project docs, and strategy notes live here. Check it when
                    a boss is beating you up.
                </li>
                <li>
                    <span className="font-semibold text-emerald-200">
                        Activity Strip
                    </span>
                    <span className="text-slate-400"> —</span>{" "}
                    The floor lights up when you trade blows with a boss. Treat it like
                    your combat log.
                </li>
            </ul>

            <p className="mt-2 text-[10px] text-slate-400">
                You can bring all of this to life by syncing real projects and clearing
                bosses — the Workshop will evolve with your progress.
            </p>
        </div>
    );
};
