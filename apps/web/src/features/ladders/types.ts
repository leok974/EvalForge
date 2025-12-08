export interface LadderUnlocks {
    type: string;
    target_world_slug?: string;
    note?: string;
}

export interface LadderNode {
    id: string;
    kind: "quest" | "boss" | "legendary_boss";
    label: string;
    order_index: number;
}

export interface LadderStage {
    stage_id: string;
    order_index: number;
    title: string;
    description: string;
    goals: string[];
    quests: string[];
    bosses: string[];
    nodes?: LadderNode[]; // Hybrid support
    unlock_condition: {
        type: string;
        boss_id?: string;
    };
    badge: {
        code: string;
        label: string;
        description: string;
    };
}

export interface LadderRewards {
    xp: number;
    titles: string[];
    unlocks: LadderUnlocks[];
}

export interface LadderSpec {
    ladder_id: string;
    slug: string;
    title: string;
    summary: string;
    recommended_entry_level: string;
    tags: string[];
    stages: LadderStage[];
    completion_rewards: LadderRewards;
}
