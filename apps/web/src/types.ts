// Senior Tier Types

export interface SeniorWorldProgress {
    world_slug: string;
    world_title: string;
    senior_track_id: string | null;
    senior_quests_total: number;
    senior_quests_completed: number;
    senior_boss_id: string | null;
    senior_boss_cleared: boolean;
}

export interface SeniorProgressResponse {
    worlds: SeniorWorldProgress[];
    total_senior_bosses: number;
    senior_bosses_cleared: number;
    legendary_trials_completed: number;
    updated_at: string;
}

export interface SeniorBossRun {
    boss_id: string;
    boss_title: string;
    world_slug: string | null;
    world_title: string | null;
    track_id: string | null;
    score: number;
    integrity: number;
    passed: boolean;
    created_at: string;
}

export interface SeniorBossRunsResponse {
    items: SeniorBossRun[];
}
