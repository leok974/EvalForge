
import React from "react";
import type { QuestState } from "@/lib/questsApi";

export const QuestStateChip: React.FC<{ state: QuestState }> = ({ state }) => {
    const config: Record<
        QuestState,
        { label: string; className: string }
    > = {
        locked: {
            label: "Locked",
            className:
                "border-slate-600/80 bg-slate-900/80 text-slate-400",
        },
        available: {
            label: "Available",
            className:
                "border-amber-400/80 bg-amber-500/10 text-amber-200",
        },
        in_progress: {
            label: "In Progress",
            className:
                "border-cyan-400/80 bg-cyan-500/10 text-cyan-200",
        },
        completed: {
            label: "Completed",
            className:
                "border-emerald-400/80 bg-emerald-500/10 text-emerald-200",
        },
        mastered: {
            label: "Mastered",
            className:
                "border-purple-400/80 bg-purple-500/10 text-purple-200",
        },
    };

    const c = config[state];

    return (
        <span
            className={`
        inline-flex items-center rounded-full border px-2 py-[1px]
        text-[9px] uppercase tracking-[0.16em]
        ${c.className}
      `}
            data-testid={`quest-state-${state}`}
        >
            {c.label}
        </span>
    );
};
