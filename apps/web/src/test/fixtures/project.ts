export type Project = {
    id: string;
    name: string;
    repo_url: string;
    sync_status: 'pending' | 'syncing' | 'ok' | 'error';
    last_sync_at: string | null;
    summary_data: { stack?: string[]; files_indexed?: number };
    codex_status?: 'complete' | 'partial' | 'missing_docs';
};

export const makeProject = (overrides: Partial<Project> = {}): Project => ({
    id: "proj-1",
    name: "Demo Project",
    repo_url: "https://github.com/example/demo",
    sync_status: 'ok',
    last_sync_at: "2026-01-01T12:00:00Z",
    summary_data: { stack: ["TypeScript", "React"], files_indexed: 10 },
    codex_status: 'complete',
    ...overrides
});

export const projectA = makeProject({ id: "proj-A", name: "Project Alpha" });
export const projectB = makeProject({ id: "proj-B", name: "Project Beta", sync_status: 'error' });
