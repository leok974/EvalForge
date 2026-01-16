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
    // New Interactive Fields
    briefing_md?: string;
    lore_md?: string;
    starter_code?: string;
    objectives?: {
        id: string;
        text: string;
        why?: string; // New: Explains the learning outcome
        validator: { kind: "regex" | "ast" | "contains"; value: string };
    }[];
    hints?: {
        id: string;
        text: string;
        type: 'concept' | 'snippet' | 'solution';
    }[];
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

export async function fetchQuest(slug: string): Promise<QuestSummary> {
    const res = await fetch(`/api/quests/${encodeURIComponent(slug)}`);
    if (!res.ok) {
        throw new Error(`Failed to fetch quest ${slug}: ${res.status}`);
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

export interface RunResult {
    passed: boolean;
    objective_results: {
        id: string;
        ok: boolean;
        detail?: string;
        line?: number;
    }[];
    stdout?: string;
    stderr?: string;
    ready_to_submit: boolean;
}

export async function runQuest(
    slug: string,
    code: string,
    language: string = "python"
): Promise<RunResult> {
    const res = await fetch(`/api/quests/${encodeURIComponent(slug)}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, language }),
    });
    if (!res.ok) throw new Error(`Failed to run quest: ${res.status}`);
    return res.json();
}

export async function unlockHint(
    slug: string,
    tier: number
): Promise<{ ok: boolean; reason?: string; max_tier?: number }> {
    const res = await fetch(`/api/quests/${encodeURIComponent(slug)}/hints/unlock?tier=${tier}`, {
        method: "POST",
    });
    if (!res.ok) throw new Error(`Failed to unlock hint: ${res.status}`);
    return res.json();
}

export interface QuestProgressV2 {
    quest_id: string;
    status: string;
    attempts_count: number;
    runs_count: number;
    hint_tier_unlocked: number;
}

export async function getQuestProgress(): Promise<QuestProgressV2[]> {
    const res = await fetch("/api/profile/progress");
    if (!res.ok) throw new Error("Failed to fetch progress");
    const data = await res.json();
    return data.quests;
}
