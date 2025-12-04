
import React from "react";
import type { QuestSubmitResult, QuestUnlockEvent } from "@/lib/questsApi";

interface QuestResultPanelProps {
    result: QuestSubmitResult | null;
}

const UnlockChip: React.FC<{ ev: QuestUnlockEvent; index: number }> = ({
    ev,
    index,
}) => {
    const label = ev.label ?? ev.id;

    if (ev.type === "boss") {
        return (
            <span
                key={`unlock-${index}`}
                data-testid={`quest-unlock-boss-${ev.id}`}
                className="
          rounded-full border border-rose-500/70
          bg-rose-500/10 px-2 py-[1px]
          text-[9px] uppercase tracking-[0.16em]
          text-rose-200 shadow-[0_0_18px_rgba(248,113,113,0.45)]
        "
            >
                Boss unlocked: {label}
            </span>
        );
    }

    if (ev.type === "layout") {
        return (
            <span
                key={`unlock-${index}`}
                data-testid={`quest-unlock-layout-${ev.id}`}
                className="
          rounded-full border border-cyan-500/70
          bg-cyan-500/10 px-2 py-[1px]
          text-[9px] uppercase tracking-[0.16em]
          text-cyan-200 shadow-[0_0_18px_rgba(34,211,238,0.45)]
        "
            >
                Layout unlocked: {label}
            </span>
        );
    }

    return null;
};

export const QuestResultPanel: React.FC<QuestResultPanelProps> = ({
    result,
}) => {
    if (!result) return null;

    const { score, passed, xp_awarded, unlock_events } = result;

    return (
        <div
            className="
        mt-2 rounded-xl border border-slate-700/80
        bg-slate-950/90 px-3 py-2 text-[11px]
        shadow-[0_10px_24px_rgba(15,23,42,0.9)]
      "
            data-testid="quest-result-panel"
        >
            <div className="flex items-center justify-between gap-2">
                <span className="text-slate-200">
                    {passed ? "Quest passed" : "Quest attempt recorded"}
                </span>
                <span className="text-[10px] text-slate-400">
                    Score:{" "}
                    <span className="text-cyan-200">
                        {score.toFixed(1)}
                    </span>
                </span>
            </div>

            <div className="mt-1 flex flex-wrap items-center gap-1.5">
                {typeof xp_awarded === "number" && xp_awarded > 0 && (
                    <span
                        data-testid="quest-result-xp"
                        className="
              rounded-full border border-emerald-400/70
              bg-emerald-500/10 px-2 py-[1px]
              text-[9px] uppercase tracking-[0.16em]
              text-emerald-200 shadow-[0_0_18px_rgba(52,211,153,0.45)]
            "
                    >
                        +{xp_awarded} XP
                    </span>
                )}

                {unlock_events?.map((ev, idx) => (
                    <UnlockChip ev={ev} index={idx} key={`${ev.type}-${ev.id}-${idx}`} />
                ))}
            </div>
        </div>
    );
};
