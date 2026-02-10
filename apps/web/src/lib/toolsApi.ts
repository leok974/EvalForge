import { safeJson } from "./safeFetch";

export interface ToolContextRequest {
    quest_slug: string;
    attempt_id?: string;
    stdout?: string;
    stderr?: string;
    failing_tests?: string[];
    user_skill_level?: string;
    files?: { path: string; content: string }[];
}

export interface ToolExplainResponse {
    summary: string;
    what_happened: string;
    why_it_failed: string;
    next_steps: string[];
    relevant_codex_refs: string[];
}

export interface ToolDebugResponse {
    summary: string;
    likely_root_causes: string[];
    fix_plan: string[];
    patch_proposal?: any;
}

export async function explainQuest(payload: ToolContextRequest): Promise<ToolExplainResponse> {
    const res = await fetch('/api/tools/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    const { ok, data, raw } = await safeJson<ToolExplainResponse>(res);
    if (!ok) {
        throw new Error(`Explain tool failed: ${res.status} ${raw?.substring(0, 100)}`);
    }
    return data!;
}

export async function debugQuest(payload: ToolContextRequest): Promise<ToolDebugResponse> {
    const res = await fetch('/api/tools/debug', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    const { ok, data, raw } = await safeJson<ToolDebugResponse>(res);
    if (!ok) {
        throw new Error(`Debug tool failed: ${res.status} ${raw?.substring(0, 100)}`);
    }
    return data!;
}
