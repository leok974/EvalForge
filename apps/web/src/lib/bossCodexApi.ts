export interface BossCodexDocMeta {
    slug: string;
    title: string;
    tier: number;
}

export interface BossCodexSummary {
    boss_id: string;
    name: string;
    world_id: string;
    tier_unlocked: number;
    kills: number;
    deaths: number;
    docs: BossCodexDocMeta[];
}

export interface BossCodexBundle {
    boss: {
        boss_id: string;
        name: string;
        world_id: string;
        tier_unlocked: number;
    };
    docs: {
        slug: string;
        title: string;
        tier: number;
        unlocked: boolean;
        body_md: string | null;
    }[];
}

export async function fetchBossList(): Promise<BossCodexSummary[]> {
    const res = await fetch("/api/codex/boss");
    if (!res.ok) throw new Error("Failed to fetch boss list");
    const json = await res.json();
    return json.bosses;
}

export async function fetchBossBundle(bossId: string): Promise<BossCodexBundle> {
    const res = await fetch(`/api/codex/boss/${bossId}`);
    if (!res.ok) throw new Error("Failed to fetch boss bundle");
    return res.json();
}
