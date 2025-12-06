export type TrackProgressDTO = {
    world_slug: string;
    track_slug: string;
    label: string;
    progress: number;
    total_quests: number;
    completed_quests: number;
};

export type WorldProgressResponse = {
    tracks: TrackProgressDTO[];
};

export async function fetchWorldProgress(): Promise<WorldProgressResponse> {
    // Assuming Vite proxy or base URL handle /api.
    // In dev, usually http://localhost:5174 proxies /api to backend.
    // We use relative path.
    const res = await fetch('/api/worlds/progress', {
        // credentials: 'include' is important if we rely on cookies, 
        // but auth_helper in mock mode might work without if header allows.
        // We'll stick to user instructions.
        // Note: If cross-origin, credentials: include is needed. Same-origin (proxy) it is default? No.
        credentials: 'include',
    });

    if (!res.ok) {
        throw new Error(`World progress fetch failed: ${res.status}`);
    }

    return res.json() as Promise<WorldProgressResponse>;
}
