import { create } from 'zustand';

export type BossStatus = 'idle' | 'active' | 'defeated' | 'failed';
export type BossDifficulty = 'normal' | 'hard';

export interface BossSpawnPayload {
    bossId: string;
    name: string;
    difficulty: BossDifficulty;
    durationSeconds: number;
    hpPenaltyOnFail: number;
    baseXpReward: number;
}

export interface BossResultPayload {
    boss_id: string;
    score: number;
    passed: boolean;
    breakdown: Record<string, number>;
    xp_awarded: number;
    integrity_delta: number;
    // Adaptive hint system
    fail_streak?: number;
    hint_codex_id?: string;
}

interface BossState {
    activeBossId: string | null;
    bossName: string | null;
    difficulty: BossDifficulty | null;
    status: BossStatus;
    lastResult: BossResultPayload | null;

    // Local mirror of HP – server is canonical, but this drives the HUD.
    integrityCurrent: number;
    integrityMax: number;

    // Boss timer deadline (epoch ms)
    deadlineTs: number | null;

    // Adaptive hint system
    hintCodexId: string | null;
    hintUnread: boolean;

    // Actions
    startBoss: (payload: BossSpawnPayload) => void;
    applyBossResult: (result: BossResultPayload) => void;
    timeoutBoss: () => void;
    reset: () => void;
    unlockHint: (codexId: string) => void;
    markHintRead: () => void;

    // Legacy support for BossPanel (can refactor later)
    bossId: string | null;
    encounterId: number | null;
    setBossResolved: (status: 'success' | 'failed') => void;
}

export const useBossStore = create<BossState>((set, get) => ({
    activeBossId: null,
    bossName: null,
    difficulty: null,
    status: 'idle',
    lastResult: null,
    integrityCurrent: 100,
    integrityMax: 100,
    deadlineTs: null,
    hintCodexId: null,
    hintUnread: false,

    // Legacy
    bossId: null,
    encounterId: null,
    setBossResolved: (status) => set({ status: status === 'success' ? 'defeated' : 'failed' }),

    startBoss: (payload) => {
        const now = Date.now();
        set({
            activeBossId: payload.bossId,
            bossId: payload.bossId, // Sync legacy
            bossName: payload.name,
            difficulty: payload.difficulty,
            status: 'active',
            lastResult: null,
            deadlineTs: now + payload.durationSeconds * 1000,
            // Reset hint state on new fight
            hintCodexId: null,
            hintUnread: false,
        });
    },

    applyBossResult: (result) => {
        const { integrityCurrent, integrityMax } = get();
        const nextHp = Math.max(
            0,
            Math.min(integrityMax, integrityCurrent + (result.integrity_delta ?? 0)),
        );

        const update: Partial<BossState> = {
            lastResult: result,
            status: result.passed ? 'defeated' : 'failed',
            activeBossId: null,
            integrityCurrent: nextHp,
            deadlineTs: null,
        };

        // If backend sends a strategy guide, mark it as new/unread
        if (result.hint_codex_id) {
            update.hintCodexId = result.hint_codex_id;
            update.hintUnread = true;
        }

        set(update as BossState);
    },

    timeoutBoss: () => {
        const { status, lastResult } = get();
        // Only punish if battle was still active.
        if (status !== 'active') return;

        // Simple timeout penalty; backend could later emit its own event.
        const timeoutResult: BossResultPayload = {
            boss_id: lastResult?.boss_id ?? 'boss-reactor-core',
            score: lastResult?.score ?? 0,
            passed: false,
            breakdown: lastResult?.breakdown ?? {},
            xp_awarded: 0,
            integrity_delta: -10,
        };

        const { integrityCurrent, integrityMax } = get();
        const nextHp = Math.max(
            0,
            Math.min(integrityMax, integrityCurrent + timeoutResult.integrity_delta),
        );

        set({
            lastResult: timeoutResult,
            status: 'failed',
            activeBossId: null,
            integrityCurrent: nextHp,
            deadlineTs: null,
        });
    },

    unlockHint: (codexId) => {
        set({
            hintCodexId: codexId,
            hintUnread: true,
        });
    },

    markHintRead: () => {
        set((state) => ({
            hintUnread: false,
            // Keep hintCodexId so HUD/chat can still open it
            hintCodexId: state.hintCodexId,
        }));
    },

    reset: () => {
        set({
            activeBossId: null,
            bossId: null,
            encounterId: null,
            status: 'idle',
            lastResult: null,
            deadlineTs: null,
        });
    },
}));

// Test helper for resetting state
export function __resetBossStoreForTests() {
    useBossStore.setState({
        activeBossId: null,
        bossName: null,
        difficulty: null,
        bossId: null,
        encounterId: null,
        status: 'idle',
        lastResult: null,
        integrityCurrent: 100,
        integrityMax: 100,
        deadlineTs: null,
    });
}
