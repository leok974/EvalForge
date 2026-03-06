import { refreshWorldProgress } from '@/features/progress/trackProgress';
import { safeJson } from '@/lib/safeFetch';

export type QuestState = "locked" | "available" | "in_progress" | "completed" | "mastered";

// ... types
export interface QuestSummary {
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
    // Quest Visibility Metadata
    questpack?: string;
    is_active?: boolean;

    // New Interactive Fields
    briefing_md?: string;
    lore_md?: string;
    starter_code?: string;

    // Phase 9.1: Tutorial Fields
    tutorial_md?: string;
    workspace_files?: { path: string; content: string; editable?: boolean }[];
    key_terms?: {
        id: string;
        term: string;
        one_liner?: string;
        codex_ref?: string;
        tags?: string[];
    }[];
    concept_tags?: string[];
    codex_references?: string[];

    // Codex Coverage Audit (from coverage tool)
    codex_coverage_score?: number;  // 0-100 score
    codex_invalid_refs?: number;     // Count of invalid refs

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
        why?: string;
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

export interface ObjectiveResult {
    id: string;
    ok: boolean;
    detail?: string;
    line?: number;
    // Actionable error fields
    kind?: 'runtime' | 'objective' | 'tests' | 'system';
    expected?: string;
    actual?: string;
    diff?: string;
}

export interface QuickFix {
    id: string;
    kind: "apply_patch" | "copy_snippet" | "navigate";
    title: string;
    why: string;
    severity: "safe" | "suggestion";
    locator?: {
        path: string;
        line: number;
        column: number;
    };
    patch?: {
        path: string;
        replacement_full_content: string;
    };
    snippet?: string;
}

// ────────────────────────────────────────────────
// SQL Preview Artifacts — canonical shapes (source of truth)
// Backend: arcade_app/services/runners/sql_preview.py
// ────────────────────────────────────────────────
/** A single statement captured in the SQLite execution trace. */
export interface SqlTraceEntry {
    idx: number;
    phase: 'setup' | 'student' | 'assert';
    sql: string;
    elapsed_ms: number;
    row_count: number | null;
    /** Column names present only when is_select=true */
    columns: string[] | null;
    /** Up to 25 preview rows, each an array of cell values */
    preview_rows: unknown[][] | null;
    error: string | null;
    is_select: boolean;
}

/**
 * The student's last SELECT result.
 * IMPORTANT: rows is an array-of-arrays, NOT array-of-objects.
 * UI must index by column position: row[colIdx].
 */
export interface SqlStudentResult {
    columns: string[];
    /** Array-of-arrays. Index by column position, not name. */
    rows: unknown[][];
    row_count: number;
    note?: string;
}

export interface SqlExplain {
    engine: 'sqlite' | string;
    statement: string;
    plan_rows: string[];
}

export interface SqlArtifacts {
    sql_student_result: SqlStudentResult;
    sql_trace: SqlTraceEntry[];
    sql_explain: SqlExplain;
}

export interface RunResult {
    passed: boolean;
    objective_results: ObjectiveResult[];
    stdout?: string | null;
    stderr?: string | null;
    ready_to_submit: boolean;
    attempt_id: string;
    run_number: number;
    duration_ms: number;
    exit_code?: number | null;
    timed_out: boolean;
    test_summary?: any;
    coach?: object;
    debrief?: DebriefData;
    diagnostics?: Diagnostic[];
    quick_fixes?: QuickFix[];
    /** For SQL quests this is SqlArtifacts; other runners may extend this. */
    artifacts?: SqlArtifacts | Record<string, unknown>;
}

export interface QuestSubmitResult {
    ok: boolean;
    quest_id: string;
    xp_awarded: number;
    mastery_awarded: number;
    objective_results: ObjectiveResult[];
    status: string;
    debrief?: DebriefData;
    diagnostics?: Diagnostic[];
    quick_fixes?: QuickFix[];
}

export interface QuestAttemptDetail {
    id: string;
    code: string;
    stdout?: string;
    stderr?: string;
    objective_results: ObjectiveResult[];
    run_number: number;
    passed: boolean;
    duration_ms: number;
    timed_out: boolean;
    is_submit: boolean;
    created_at: string;
    debrief?: DebriefData;
    diagnostics?: Diagnostic[];
    quick_fixes?: QuickFix[];
}

export async function fetchQuests(worldId?: string): Promise<QuestSummary[]> {
    const params = worldId ? `?world_id=${encodeURIComponent(worldId)}` : "";
    // Note: Backend router expects trailing slash for list endpoint
    const res = await fetch(`/api/quests${params}`);
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

    // MOCK DATA INJECTION for Starter Quest
    if (data && (data.id === 1 || data.slug === 'first-sparks')) {
        data.starter_code = `# IGNITION SEQUENCE\n# -----------------\ndef main():\n    print("Ignition sequence started...")\n    for i in range(3, 0, -1):\n        print(f"T-minus {i}")\n    print("Liftoff!")\n\nif __name__ == "__main__":\n    main()\n`;
        data.briefing_md = `### SIGNAL INTERCEPTED
**Source**: Foundry Ignition Console
**Priority**: CRITICAL

The automated ignition systems are offline. We need to manually override the launch sequence to deploy the Agentic Core.

**Your mission**: Write a script that initiates the countdown and confirms liftoff.`;
        data.lore_md = `> *The Foundry was once the heart of the old web, before the stagnation. Now it's just cold iron and silence. Rekindling it requires more than just power; it requires intent.*`;
        data.objectives = [
            { id: 'def_main', text: 'Define a main() function', why: 'Entry point for the ignition script', validator: { kind: 'regex', value: 'def main' } },
            { id: 'loop', text: 'Countdown loop (T-minus)', why: 'Iterates through the launch sequence', validator: { kind: 'contains', value: 'for' } },
            { id: 'print', text: 'Confirm Liftoff', why: 'Signal the core is active', validator: { kind: 'contains', value: 'Liftoff' } }
        ];
        data.hints = [
            { id: 'h1', type: 'concept', text: 'In Python, a standard entry point often looks like `if __name__ == "__main__":`' },
            { id: 'h2', type: 'snippet', text: '```python\nfor i in range(3, 0, -1):\n    print(f"T-minus {i}")\n```' },
            { id: 'h3', type: 'solution', text: 'Copy the starter code completely if you are stuck!' }
        ];
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
    // Phase 8.x PR 3: Generate idempotency key
    const idempotency_key = crypto.randomUUID();

    const res = await fetch(
        `/api/quests/${encodeURIComponent(slug)}/submit`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ code, language, workspace, idempotency_key }),
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
    mode: "validate" | "execute" | "tests" = "execute",
    workspaceConfig?: { entrypoint: string; files: { path: string; content: string }[] }
): Promise<RunResult> {
    const payload: any = { code, language, mode };
    if (workspaceConfig) {
        payload.entrypoint = workspaceConfig.entrypoint;
        payload.workspace = workspaceConfig.files;
    }

    // Phase 8.x PR 3: Generate idempotency key
    payload.idempotency_key = crypto.randomUUID();

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
