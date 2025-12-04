
import React, { useEffect, useMemo, useState } from "react";
import {
    fetchQuests,
    acceptQuest,
    QuestSummary,
    QuestState,
} from "@/lib/questsApi";
import { QuestStateChip } from "./quests/QuestStateChip";
import { QUEST_UPDATED_EVENT } from "@/lib/questsEvents";
import type { QuestUpdatedDetail } from "@/lib/questsEvents";

interface QuestBoardProps {
    worldId?: string;
    onOpenQuest?: (quest: QuestSummary) => void;
}

type FilterTrackId = "all" | string;

function stateRank(state: QuestState): number {
    switch (state) {
        case "locked":
            return 0;
        case "available":
            return 1;
        case "in_progress":
            return 2;
        case "completed":
            return 3;
        case "mastered":
            return 4;
        default:
            return 0;
    }
}

export const QuestBoard: React.FC<QuestBoardProps> = ({
    worldId,
    onOpenQuest,
}) => {
    const [quests, setQuests] = useState<QuestSummary[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const [activeTrack, setActiveTrack] = useState<FilterTrackId>("all");
    const [acceptingSlug, setAcceptingSlug] = useState<string | null>(null);
    const [progressPulse, setProgressPulse] = useState(false);

    useEffect(() => {
        let cancelled = false;
        setLoading(true);
        setError(null);
        fetchQuests(worldId)
            .then((data) => {
                if (!cancelled) {
                    setQuests(data);
                }
            })
            .catch((err) => {
                if (!cancelled) {
                    setError(err.message ?? "Failed to load quests");
                }
            })
            .finally(() => {
                if (!cancelled) setLoading(false);
            });

        return () => {
            cancelled = true;
        };
    }, [worldId]);

    useEffect(() => {
        if (typeof window === "undefined") return;

        const handler = (event: Event) => {
            const custom = event as CustomEvent<QuestUpdatedDetail>;
            const updated = custom.detail?.quest;
            if (!updated) return;

            setQuests((prev) => {
                const existing = prev.find((q) => q.id === updated.id);
                if (!existing) return prev;

                const improved =
                    stateRank(updated.state) > stateRank(existing.state);

                const next = prev.map((q) =>
                    q.id === updated.id ? { ...q, ...updated } : q
                );

                if (improved) {
                    setProgressPulse(true);
                    setTimeout(() => setProgressPulse(false), 280);
                }

                return next;
            });
        };

        window.addEventListener(QUEST_UPDATED_EVENT, handler);
        return () => window.removeEventListener(QUEST_UPDATED_EVENT, handler);
    }, []);

    // Derive list of tracks and current filter
    const trackIds = useMemo(() => {
        const set = new Set<string>();
        for (const q of quests) set.add(q.track_id);
        return Array.from(set).sort();
    }, [quests]);

    const filteredQuests = useMemo(() => {
        if (activeTrack === "all") return quests;
        return quests.filter((q) => q.track_id === activeTrack);
    }, [quests, activeTrack]);

    // Overall progress metrics (for the current world + filter)
    const progress = useMemo(() => {
        if (!quests.length) {
            return {
                total: 0,
                completed: 0,
                mastered: 0,
                percentCompleted: 0,
                percentMastered: 0,
            };
        }

        const withinFilter =
            activeTrack === "all"
                ? quests
                : quests.filter((q) => q.track_id === activeTrack);

        const total = withinFilter.length;
        const completed = withinFilter.filter((q) =>
            ["completed", "mastered"].includes(q.state)
        ).length;
        const mastered = withinFilter.filter((q) => q.state === "mastered").length;

        const percentCompleted = total ? Math.round((completed / total) * 100) : 0;
        const percentMastered = total ? Math.round((mastered / total) * 100) : 0;

        return {
            total,
            completed,
            mastered,
            percentCompleted,
            percentMastered,
        };
    }, [quests, activeTrack]);

    const handleAcceptOrContinue = async (quest: QuestSummary) => {
        // locked → do nothing for now
        if (quest.state === "locked") return;

        // For in_progress/completed/mastered: just fire onOpenQuest
        if (quest.state !== "available") {
            onOpenQuest?.(quest);
            return;
        }

        // available → accept, then open
        try {
            setAcceptingSlug(quest.slug);
            const updated = await acceptQuest(quest.slug);

            // Patch local quests array
            setQuests((prev) =>
                prev.map((q) => (q.slug === updated.slug ? updated : q))
            );

            onOpenQuest?.(updated);
        } catch (err) {
            console.error("Failed to accept quest", err);
            // optional: surface toast via your global toast system
        } finally {
            setAcceptingSlug(null);
        }
    };

    if (loading) {
        return (
            <div className="text-[11px] text-slate-400">
                Loading quests…
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-[11px] text-rose-300">
                Failed to load quests: {error}
            </div>
        );
    }

    if (!quests.length) {
        return (
            <div className="text-[11px] text-slate-400">
                No quests found for this world yet.
            </div>
        );
    }

    return (
        <div className="flex h-full flex-col gap-2" data-testid="quest-board-root">
            {/* Header: filters + progress meter */}
            <header className={`
                flex flex-col gap-1.5 border-b border-slate-800 pb-1.5
                transition-transform duration-150
                ${progressPulse ? "animate-[wiggle_0.25s_ease-in-out]" : ""}
            `}>
                {/* Track filter pills */}
                <div className="flex flex-wrap items-center gap-1.5 text-[10px]">
                    <span className="text-slate-400">Track:</span>
                    <button
                        type="button"
                        onClick={() => setActiveTrack("all")}
                        className={`
              rounded-full border px-2 py-[1px]
              ${activeTrack === "all"
                                ? "border-cyan-400/80 bg-cyan-500/10 text-cyan-200"
                                : "border-slate-700/80 bg-slate-950/80 text-slate-300 hover:border-slate-500"
                            }
            `}
                        data-testid="quest-filter-all"
                    >
                        All ({quests.length})
                    </button>
                    {trackIds.map((track) => {
                        const count = quests.filter((q) => q.track_id === track).length;
                        return (
                            <button
                                key={track}
                                type="button"
                                onClick={() => setActiveTrack(track)}
                                className={`
                  rounded-full border px-2 py-[1px]
                  ${activeTrack === track
                                        ? "border-cyan-400/80 bg-cyan-500/10 text-cyan-200"
                                        : "border-slate-700/80 bg-slate-950/80 text-slate-300 hover:border-slate-500"
                                    }
                `}
                                data-testid={`quest-filter-${track}`}
                            >
                                {track} ({count})
                            </button>
                        );
                    })}
                </div>

                {/* Progress meter */}
                <div className="flex items-center justify-between gap-2 text-[10px]">
                    <div className="flex flex-wrap items-center gap-1.5 text-slate-400">
                        <span>
                            Completed:{" "}
                            <span className="text-emerald-200">
                                {progress.completed}/{progress.total}
                            </span>{" "}
                            ({progress.percentCompleted}%)
                        </span>
                        <span>|</span>
                        <span>
                            Mastered:{" "}
                            <span className="text-purple-200">
                                {progress.mastered}/{progress.total}
                            </span>{" "}
                            ({progress.percentMastered}%)
                        </span>
                    </div>
                    <div className="hidden h-1.5 flex-1 overflow-hidden rounded-full bg-slate-800 sm:block">
                        <div
                            className="h-full bg-emerald-500/80"
                            style={{ width: `${progress.percentCompleted}%` }}
                        />
                    </div>
                </div>
            </header>

            {/* Quest list */}
            <div className="flex-1 space-y-2 overflow-auto" data-testid="quest-board">
                {filteredQuests.map((q) => {
                    const isAccepting = acceptingSlug === q.slug;
                    const label =
                        q.state === "locked"
                            ? "Locked"
                            : q.state === "available"
                                ? "Accept"
                                : q.state === "in_progress"
                                    ? "Continue"
                                    : q.state === "completed"
                                        ? "Replay"
                                        : "Replay (Mastered)";

                    const buttonDisabled = q.state === "locked" || isAccepting;

                    return (
                        <article
                            key={q.id}
                            className={`
                rounded-xl border border-slate-700/80
                bg-slate-950/80 px-3 py-2
                shadow-[0_12px_26px_rgba(15,23,42,0.75)]
              `}
                            data-testid={`quest-card-${q.slug}`}
                        >
                            <div className="flex items-center justify-between gap-2">
                                <div className="flex flex-col">
                                    <span className="text-[12px] font-semibold text-slate-50">
                                        {q.title}
                                    </span>
                                    <span className="text-[10px] text-slate-400">
                                        {q.short_description}
                                    </span>
                                </div>
                                <QuestStateChip state={q.state} />
                            </div>

                            <div className="mt-1 flex items-center justify-between gap-2">
                                <div className="flex flex-wrap items-center gap-1.5 text-[10px] text-slate-500">
                                    <span>XP: {q.base_xp_reward}</span>
                                    {q.mastery_xp_bonus > 0 && (
                                        <span className="text-purple-300/90">
                                            +{q.mastery_xp_bonus} mastery
                                        </span>
                                    )}
                                    {q.unlocks_boss_id && (
                                        <span className="rounded-full border border-rose-500/60 bg-rose-500/10 px-2 py-[1px] text-[9px] uppercase tracking-[0.16em] text-rose-200">
                                            Boss: {q.unlocks_boss_id}
                                        </span>
                                    )}
                                    {q.unlocks_layout_id && (
                                        <span className="rounded-full border border-cyan-500/60 bg-cyan-500/10 px-2 py-[1px] text-[9px] uppercase tracking-[0.16em] text-cyan-200">
                                            Unlocks: {q.unlocks_layout_id}
                                        </span>
                                    )}
                                </div>

                                <button
                                    type="button"
                                    onClick={() => handleAcceptOrContinue(q)}
                                    disabled={buttonDisabled}
                                    data-testid={`quest-action-${q.slug}`}
                                    className={`
                    rounded-full border px-2.5 py-[3px] text-[10px]
                    ${buttonDisabled
                                            ? "border-slate-700 bg-slate-900 text-slate-500 cursor-not-allowed"
                                            : q.state === "available"
                                                ? "border-amber-400 bg-amber-500/10 text-amber-100 hover:bg-amber-500/20"
                                                : "border-cyan-400 bg-cyan-500/10 text-cyan-100 hover:bg-cyan-500/20"
                                        }
                  `}
                                >
                                    {isAccepting ? "…" : label}
                                </button>
                            </div>
                        </article>
                    );
                })}
            </div>
        </div>
    );
};
