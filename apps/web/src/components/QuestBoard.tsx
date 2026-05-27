
import React, { useEffect, useMemo, useState } from "react";
import {
    fetchQuests,
    acceptQuest,
    QuestSummary,
    QuestState,
} from "@/lib/questsApi";
// import { QuestStateChip } from "./quests/QuestStateChip";
import { QUEST_UPDATED_EVENT } from "@/lib/questsEvents";
import type { QuestUpdatedDetail } from "@/lib/questsEvents";

import { useNavigate } from "react-router-dom";
import { useWorkshopCatalog } from "@/features/workshop/WorkshopCatalogContext";
import { isGodModeEnabledFromEnv } from "@/config/devFlags";

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
    const navigate = useNavigate();
    const {
        getTracksForWorld,
        resolveTrackName,
        resolveWorldName,
        resolveCanonicalTrackId,
        worlds,
        tracks: allTracks
    } = useWorkshopCatalog();

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
                    // NORMALIZE TRACK IDs (Fundamentals -> Python Fundamentals)
                    // This allows the frontend to group quests under the canonical track
                    // even if the backend returns legacy IDs.
                    const normalized = data.map(q => {
                        let state = q.state;
                        // Bypass locks locally if God Mode is ON
                        if (state === 'locked' && isGodModeEnabledFromEnv()) {
                            state = 'available';
                        }
                        return {
                            ...q,
                            state,
                            track_id: resolveCanonicalTrackId(q.track_id)
                        };
                    });
                    setQuests(normalized);
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
    }, [worldId, resolveCanonicalTrackId]);

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

    // USE CATALOG FOR TRACKS (Source of Truth)
    const catalogTracks = useMemo(() => {
        if (!worldId) return [];
        return getTracksForWorld(worldId);
    }, [worldId, getTracksForWorld]);

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

        // For in_progress/completed/mastered: navigate
        if (quest.state !== "available") {
            // Use callback if provided (legacy), otherwise navigate
            if (onOpenQuest) {
                onOpenQuest(quest);
            } else {
                navigate(`quests/${quest.slug}`);
            }
            return;
        }

        // available → accept, then navigate
        try {
            setAcceptingSlug(quest.slug);
            const updated = await acceptQuest(quest.slug);

            // Patch local quests array
            setQuests((prev) =>
                prev.map((q) => (q.slug === updated.slug ? updated : q))
            );

            if (onOpenQuest) {
                onOpenQuest(updated);
            } else {
                navigate(`quests/${updated.slug}`);
            }
        } catch (err) {
            console.error("Failed to accept quest", err);
            // optional: surface toast via your global toast system
        } finally {
            setAcceptingSlug(null);
        }
    };

    // Helpers for Resolving Names
    const getWorldObj = (id: string) => worlds.find(w => w.world_id === id);
    const getTrackObj = (id: string) => allTracks.find(t => t.track_id === id);

    if (loading) {
        return (
            <div className="text-[11px] text-slate-400">
                Loading quests…
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-[11px] text-red-400">
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
                    {/* Render Catalog Tracks (Active Only) */}
                    {catalogTracks.map((track) => {
                        const count = quests.filter((q) => q.track_id === track.track_id).length;
                        if (count === 0 && activeTrack !== track.track_id) return null; // Hide empty tracks? Or show 0?

                        return (
                            <button
                                key={track.track_id}
                                type="button"
                                onClick={() => setActiveTrack(track.track_id)}
                                className={`
                  rounded-full border px-2 py-[1px]
                  ${activeTrack === track.track_id
                                        ? "border-cyan-400/80 bg-cyan-500/10 text-cyan-200"
                                        : "border-slate-700/80 bg-slate-950/80 text-slate-300 hover:border-slate-500"
                                    }
                `}
                                data-testid={`quest-filter-${track.track_id}`}
                            >
                                {resolveTrackName(track)} ({count})
                            </button>
                        );
                    })}
                </div>

                {/* Progress meter */}
                <div className="flex items-center justify-between gap-2 text-[10px]">
                    <div className="flex items-center gap-2">
                        <span className="rounded-full bg-emerald-950/50 border border-emerald-500/30 px-2 py-0.5 text-emerald-400 font-mono uppercase tracking-wider text-[9px]">
                            Showing: Active Quests
                        </span>
                        <div className="flex flex-wrap items-center gap-1.5 text-slate-400">
                            <span>
                                Completed:{" "}
                                <span className="text-emerald-200">
                                    {progress.completed}/{progress.total}
                                </span>{" "}
                                ({progress.percentCompleted}%)
                            </span>
                        </div>
                    </div>
                </div>
            </header>

            {/* Quest list */}
            <ul className="flex-1 space-y-2 overflow-auto pr-1" data-testid="quest-board">
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
                        <li
                            key={q.id}
                            className={`
                                mb-1 rounded-2xl border border-slate-800/70
                                bg-slate-950/60 px-4 py-3
                                shadow-sm shadow-slate-950/60 transition-all hover:bg-slate-900/40
                            `}
                            data-testid={`quest-card-${q.slug}`}
                        >
                            <div className="flex items-start justify-between gap-4">
                                <div className="flex flex-col gap-1.5 flex-1">
                                    {/* Title row */}
                                    <div className="flex flex-wrap items-center gap-2">
                                        <h3 className="text-sm font-semibold text-slate-50">
                                            {q.title}
                                        </h3>

                                        {/* Boss badge (prominent — unlocks a boss fight) */}
                                        {q.unlocks_boss_id && (
                                            <span className="rounded-full border border-red-400/70 bg-red-950/30 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide text-red-300">
                                                Boss
                                            </span>
                                        )}
                                    </div>

                                    {/* Description */}
                                    {q.short_description && (
                                        <p className="text-xs text-slate-400 leading-snug">
                                            {q.short_description}
                                        </p>
                                    )}

                                    {/* Badge hierarchy: track pill > tier badge > content tags */}
                                    <div className="flex flex-wrap items-center gap-1.5">
                                        {/* PRIMARY: Track pill */}
                                        <span
                                            className="rounded-full border border-workshop-cyan/40 bg-cyan-950/30 px-2.5 py-0.5 text-[10px] font-medium text-workshop-cyan"
                                            title={`Track: ${q.track_id}`}
                                        >
                                            {getTrackObj(q.track_id)
                                                ? resolveTrackName(getTrackObj(q.track_id)!)
                                                : q.track_id}
                                        </span>

                                        {/* SECONDARY: Tier badge (derived from track suffix) */}
                                        {(() => {
                                            const tid = q.track_id || '';
                                            if (tid.endsWith('-systems')) return (
                                                <span className="rounded-full border border-violet-400/40 bg-violet-950/30 px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wide text-violet-400">
                                                    Systems
                                                </span>
                                            );
                                            if (tid.endsWith('-ignition') || tid.endsWith('-selenium')) return (
                                                <span className="rounded-full border border-blue-400/40 bg-blue-950/30 px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wide text-blue-400">
                                                    Ignition
                                                </span>
                                            );
                                            if (tid.endsWith('-boss')) return (
                                                <span className="rounded-full border border-red-400/40 bg-red-950/30 px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wide text-red-400">
                                                    Boss
                                                </span>
                                            );
                                            if (tid.endsWith('-foundry')) return (
                                                <span className="rounded-full border border-slate-500/40 bg-slate-900/30 px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wide text-slate-500">
                                                    Foundry
                                                </span>
                                            );
                                            return null;
                                        })()}

                                        {/* TERTIARY: Content tags (subordinate) */}
                                        {q.concept_tags && q.concept_tags.length > 0 && (
                                            q.concept_tags.slice(0, 3).map(tag => (
                                                <span
                                                    key={tag}
                                                    className="rounded border border-zinc-700/50 px-1.5 py-0 text-[9px] text-zinc-600"
                                                >
                                                    {tag}
                                                </span>
                                            ))
                                        )}

                                        {/* Dev-only: Codex Coverage */}
                                        {q.codex_coverage_score !== undefined && (
                                            <span
                                                className={`
                                                    rounded border px-1.5 py-0 text-[9px]
                                                    ${q.codex_coverage_score >= 90
                                                        ? 'border-emerald-600/50 text-emerald-600'
                                                        : q.codex_coverage_score >= 70
                                                            ? 'border-blue-600/50 text-blue-600'
                                                            : q.codex_coverage_score > 0
                                                                ? 'border-amber-600/50 text-amber-600'
                                                                : 'border-slate-600/50 text-slate-600'
                                                    }
                                                `}
                                                title={`Codex coverage: ${q.codex_coverage_score}/100`}
                                            >
                                                📚 {q.codex_coverage_score}
                                            </span>
                                        )}
                                        {q.codex_invalid_refs && q.codex_invalid_refs > 0 && (
                                            <span
                                                className="rounded border border-red-600/50 px-1.5 py-0 text-[9px] text-red-500"
                                                title={`${q.codex_invalid_refs} invalid Codex reference(s)`}
                                            >
                                                ⚠️ {q.codex_invalid_refs}
                                            </span>
                                        )}
                                    </div>

                                    <div className="mt-1 flex flex-wrap items-center gap-3 text-[11px] text-slate-400">
                                        <span>XP: {q.base_xp_reward}–{q.base_xp_reward + (q.mastery_xp_bonus || 0)}</span>
                                        <span className="h-1 w-1 rounded-full bg-slate-600" />
                                        <span>+{q.mastery_xp_bonus} mastery</span>
                                    </div>
                                </div>

                                <div className="flex flex-col items-end gap-1 shrink-0">
                                    <button
                                        type="button"
                                        onClick={() => handleAcceptOrContinue(q)}
                                        disabled={buttonDisabled}
                                        data-testid={`quest-action-${q.slug}`}
                                        className={`
                                            rounded-full border px-3 py-1 text-[11px] text-slate-200 transition-all
                                            ${buttonDisabled
                                                ? "border-slate-600/50 text-slate-500 opacity-40 cursor-not-allowed"
                                                : "border-slate-600 hover:border-emerald-400 hover:text-emerald-200"
                                            }
                                        `}
                                    >
                                        {isAccepting ? "..." : q.state === "locked" ? "Locked" : label}
                                    </button>
                                </div>
                            </div>
                        </li>
                    );
                })}
            </ul>
        </div>
    );
};

