import { refreshWorldProgress } from '@/features/progress/trackProgress';

export type QuestState = "locked" | "available" | "in_progress" | "completed" | "mastered";

export interface QuestSummary {
    // ... existing types ...
    id: number;
    slug: string;
    world_id: string;
    track_id: string;
    order_index: number;
    title: string;
    short_description: string;
    state: QuestState;
    best_score: number | null;
    attempts: number;
    unlocks_boss_id?: string | null;
    unlocks_layout_id?: string | null;
    base_xp_reward: number;
    mastery_xp_bonus: number;
}

export interface QuestUnlockEvent {
    type: "boss" | "layout";
    id: string;
    label?: string;
}

export interface QuestSubmitResult {
    quest: QuestSummary;
    score: number;
    passed: boolean;
    xp_awarded?: number;
    unlock_events?: QuestUnlockEvent[];
    profile?: {
        xp?: number;
        flags?: Record<string, unknown>;
    };
}

export async function fetchQuests(worldId?: string): Promise<QuestSummary[]> {
    const params = worldId ? `?world_id=${encodeURIComponent(worldId)}` : "";
    const res = await fetch(`/api/quests/${params}`);
    if (!res.ok) {
        throw new Error(`Failed to fetch quests: ${res.status}`);
    }
    return res.json();
}

export async function acceptQuest(slug: string): Promise<QuestSummary> {
    const res = await fetch(`/api/quests/${encodeURIComponent(slug)}/accept`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    });
    if (!res.ok) {
        throw new Error(`Failed to accept quest ${slug}: ${res.status}`);
    }
    return res.json();
}


export async function submitQuestSolution(
    slug: string,
    code: string,
    language?: string
): Promise<QuestSubmitResult> {
    const res = await fetch(
        `/api/quests/${encodeURIComponent(slug)}/submit`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ code, language }),
        }
    );
    if (!res.ok) {
        throw new Error(`Failed to submit quest ${slug}: ${res.status}`);
    }

    // Fire off a progress refresh without blocking
    refreshWorldProgress().catch((err) => {
        console.warn('World progress refresh failed after quest completion', err);
    });

    return res.json();
}
