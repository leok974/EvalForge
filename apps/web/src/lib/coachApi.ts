
import { safeJson } from "./safeFetch";

export interface CoachRequest {
    mode: 'explain' | 'debug' | 'auto';
    world: string;
    quest_slug: string;
    student_mode: boolean;
    runner_result?: any;
    failing_tests_text?: string;
    terminal_output_text?: string;
    selected_paths?: string[];
    workspace_files: { path: string; content: string }[];
    attempt_id?: string;
    // Context anchoring — must match backend CoachRequest fields
    entrypoint_path?: string;   // e.g. "task.sql" or "task.py"
    language?: string;           // e.g. "sql", "python"
    run_passed?: boolean;        // true = last run was a clean pass
}

export interface CoachResponse {
    mode: 'explain' | 'debug';
    summary_md: string;
    hypotheses: { title: string; evidence: string[] }[];
    next_steps: { label: string; action: string; target?: string }[];
    patch?: { unified_diff: string };
    confidence: number;
    safety: { solution_leak_risk: string; blocked: boolean };
    primary_error?: { code: string; message: string };
    evidence: string[];
    failure_class?: string;
}

export async function fetchCoachFeedback(payload: CoachRequest): Promise<CoachResponse> {
    // Graceful check for config (optional, backend also checks)
    // if (import.meta.env.VITE_EF_COACH_ENABLED === '0') ...

    const res = await fetch('/api/coach', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    const { ok, data, raw } = await safeJson<CoachResponse>(res);
    if (!ok) {
        throw new Error(`Coach API failed: ${res.status} ${raw?.substring(0, 100)}`);
    }
    return data!;
}
