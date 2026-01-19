import { refreshWorldProgress } from '@/features/progress/trackProgress';
import { safeJson } from '@/lib/safeFetch';

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
    language?: string;
    // New Interactive Fields
    briefing_md?: string;
    lore_md?: string;
    starter_code?: string;

    // Phase 6: Multi-File
    workspace?: {
        entrypoint: string;
        files: { path: string; content: string; editable?: boolean }[];
    };
    grading?: {
        mode: "run" | "tests";
        // Hidden tests not leaked to client
    };

    objectives?: {
        id: string;
        text: string;
        why?: string; // New: Explains the learning outcome
        validator: { kind: "regex" | "ast" | "contains" | "tests_pass"; value: string };
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

export interface Diagnostic {
    path: string;
    line: number;
    column: number;
    severity: "error" | "warning";
    kind: "syntax" | "runtime" | "test";
    message: string;
}

export interface DebriefData {
    title: string;
    passed_objectives: string[];
    objective_titles: { id: string; title: string }[];
    tests?: { passed: number; failed: number; mode: string };
    learning_points: string[];
    next?: {
        quest_id: string; // Slug
        title: string;
        why: string;
    } | null;
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
    coach?: any; // CoachData
    debrief?: DebriefData;
    diagnostics?: Diagnostic[];
}

// ... (fetch endpoints)

// ...

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
    // New Artifact fields
    attempt_id?: string;
    run_number?: number;
    duration_ms?: number;
    exit_code?: number;
    timed_out?: boolean;
    test_summary?: any;
    coach?: any;
    debrief?: DebriefData;
    diagnostics?: Diagnostic[];
}

// ...

export interface QuestAttemptDetail extends QuestAttemptSummary {
    code: string;
    stdout?: string;
    stderr?: string;
    objective_results: {
        id: string;
        ok: boolean;
        detail?: string;
        line?: number;
    }[];
    debrief_json?: DebriefData;
    diagnostics_json?: Diagnostic[];
}

export async function fetchQuests(worldId?: string): Promise<QuestSummary[]> {
    const params = worldId ? `?world_id=${encodeURIComponent(worldId)}` : "";
    // Note: Backend router expects trailing slash for list endpoint
    const res = await fetch(`/api/quests/${params}`);
    const { ok, data, raw } = await safeJson<QuestSummary[]>(res);
    if (!ok) {
        throw new Error(`Failed to fetch quests: ${res.status} ${raw?.substring(0, 100)}`);
    }
    return data!;
}

export async function fetchQuest(slug: string): Promise<QuestSummary> {
    const res = await fetch(`/api/quests/${encodeURIComponent(slug)}`);
    const { ok, data, raw } = await safeJson<QuestSummary>(res);
    if (!ok) {
        throw new Error(`Failed to fetch quest ${slug}: ${res.status} ${raw?.substring(0, 100)}`);
    }
    return data!;
}

export async function acceptQuest(slug: string): Promise<QuestSummary> {
    const res = await fetch(`/api/quests/${encodeURIComponent(slug)}/accept`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    });
    const { ok, data, raw } = await safeJson<QuestSummary>(res);
    if (!ok) {
        throw new Error(`Failed to accept quest ${slug}: ${res.status} ${raw?.substring(0, 100)}`);
    }
    return data!;
}


export async function submitQuestSolution(
    slug: string,
    code: string,
    language?: string,
    workspace?: { entrypoint: string; files: { path: string; content: string }[] }
): Promise<QuestSubmitResult> {
    const res = await fetch(
        `/api/quests/${encodeURIComponent(slug)}/submit`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ code, language, workspace }),
        }
    );
    const { ok, data, raw } = await safeJson<QuestSubmitResult>(res);
    if (!ok) {
        throw new Error(`Failed to submit quest ${slug}: ${res.status} ${raw?.substring(0, 100)}`);
    }

    // Fire off a progress refresh without blocking
    refreshWorldProgress().catch((err) => {
        console.warn('World progress refresh failed after quest completion', err);
    });

    return data!;
}

export async function runQuest(
    slug: string,
    code: string,
    language: string = "python",
    mode: "validate" | "execute" = "execute",
    workspaceConfig?: { entrypoint: string; files: { path: string; content: string }[] }
): Promise<RunResult> {
    const payload: any = { code, language, mode };
    if (workspaceConfig) {
        payload.entrypoint = workspaceConfig.entrypoint;
        payload.workspace = workspaceConfig.files;
    }

    const res = await fetch(`/api/quests/${encodeURIComponent(slug)}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    const { ok, data, raw } = await safeJson<RunResult>(res);
    if (!ok) throw new Error(`Failed to run quest: ${res.status} ${raw?.substring(0, 100)}`);
    return data!;
}

export interface QuestAttemptSummary {
    id: string;
    created_at: string;
    run_number: number;
    passed: boolean;
    is_submit: boolean;
    duration_ms: number;
    timed_out: boolean;
    exit_code: number;
}




export async function fetchQuestAttempts(slug: string, limit: number = 25): Promise<QuestAttemptSummary[]> {
    const res = await fetch(`/api/quests/${encodeURIComponent(slug)}/attempts?limit=${limit}`);
    if (!res.ok) throw new Error(`Failed to fetch attempts: ${res.status}`);
    return res.json();
}

export async function fetchQuestAttempt(slug: string, attemptId: string): Promise<QuestAttemptDetail> {
    const res = await fetch(`/api/quests/${encodeURIComponent(slug)}/attempts/${encodeURIComponent(attemptId)}`);
    if (!res.ok) throw new Error(`Failed to fetch attempt detail: ${res.status}`);
    return res.json();
}

// ... (existing code for unlockHint, etc.)
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

// ... (rest of file)

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
