import { useState, useEffect } from 'react';

export interface QASummary {
    generated_at: string;
    tracks: Array<{
        world_id: string;
        track_id: string;
        quests_total: number;
        healthy: number;
        unhealthy: number;
        unknown: number;
    }>;
    global: {
        quests_total: number;
        healthy: number;
        unhealthy: number;
        unknown: number;
    };
}

export interface QuestHealth {
    slug: string;
    title: string;
    world_id: string;
    track_id: string;
    language: string;
    health_status: 'healthy' | 'unhealthy' | 'running' | 'unknown';
    last_run_at: string | null;
    last_run_variant: string | null;
}

export interface QARunRequest {
    quest_id: string;
    variant: 'starter' | 'solution' | 'integrity';
}

export interface QARunResponse {
    id: string;
    quest_slug: string;
    variant: string;
    status: 'queued' | 'running' | 'finished' | 'failed';
    duration_ms: number | null;
    result: any;
    logs: string | null;
    diagnostics: any;
    test_summary: any;
    created_at: string;
}

const API_BASE = '/api/qa';

export async function getQASummary(): Promise<QASummary> {
    const response = await fetch(`${API_BASE}/summary`);
    if (!response.ok) {
        throw new Error(`Failed to fetch QA summary: ${response.statusText}`);
    }
    return response.json();
}

export async function getQAQuests(filters?: {
    world_id?: string;
    track_id?: string;
    language?: string;
    status?: string;
    q?: string;
}): Promise<{ quests: QuestHealth[] }> {
    const params = new URLSearchParams();
    if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
            if (value) params.append(key, value);
        });
    }

    const url = `${API_BASE}/quests${params.toString() ? `?${params.toString()}` : ''}`;
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`Failed to fetch QA quests: ${response.statusText}`);
    }
    return response.json();
}

export async function getQAArtifact(filename: string): Promise<any> {
    const response = await fetch(`${API_BASE}/artifacts/${filename}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch artifact: ${response.statusText}`);
    }
    return response.json();
}

export async function runQATest(request: QARunRequest): Promise<{ run_id: string; status: string }> {
    const response = await fetch(`${API_BASE}/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request)
    });

    if (!response.ok) {
        throw new Error(`Failed to run QA test: ${response.statusText}`);
    }
    return response.json();
}

export async function getQARun(runId: string): Promise<QARunResponse> {
    const response = await fetch(`${API_BASE}/runs/${runId}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch QA run: ${response.statusText}`);
    }
    return response.json();
}

export async function pollQARun(
    runId: string,
    onUpdate: (run: QARunResponse) => void,
    intervalMs: number = 1000
): Promise<QARunResponse> {
    return new Promise((resolve, reject) => {
        const poll = async () => {
            try {
                const run = await getQARun(runId);
                onUpdate(run);

                if (run.status === 'finished' || run.status === 'failed') {
                    resolve(run);
                } else {
                    setTimeout(poll, intervalMs);
                }
            } catch (error) {
                reject(error);
            }
        };

        poll();
    });
}
