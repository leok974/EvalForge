/**
 * Shared BossStore test double.
 * If you change the real boss store shape, update this FIRST
 * before sprinkling new ad-hoc mocks.
 */
import { vi } from 'vitest';

export type MockBossRun = {
    id: string;
    boss_slug: string;
    score: number;
    grade: string;
    passed: boolean;
    timestamp: number;
};

export type MockBossStoreState = {
    // State
    currentBossSlug: string | null;
    status: 'idle' | 'active' | 'victory' | 'defeat';
    maxHp: number;
    hp: number;
    runs: MockBossRun[]; // History

    // Actions
    startBoss: (slug: string) => void;
    damageBoss: (amount: number) => void;
    resetBoss: () => void;
    registerRun: (run: MockBossRun) => void;
};

export function createMockBossStoreState(
    overrides: Partial<MockBossStoreState> = {}
): MockBossStoreState {
    const state: MockBossStoreState = {
        currentBossSlug: null,
        status: 'idle',
        maxHp: 100,
        hp: 100,
        runs: [],

        startBoss: vi.fn((slug: string) => {
            state.currentBossSlug = slug;
            state.status = 'active';
            state.hp = state.maxHp;
        }),

        damageBoss: vi.fn((amount: number) => {
            state.hp = Math.max(0, state.hp - amount);
            if (state.hp === 0) state.status = 'victory';
        }),

        resetBoss: vi.fn(() => {
            state.currentBossSlug = null;
            state.status = 'idle';
            state.hp = state.maxHp;
        }),

        registerRun: vi.fn((run: MockBossRun) => {
            state.runs.push(run);
        }),

        ...overrides,
    };

    return state;
}
