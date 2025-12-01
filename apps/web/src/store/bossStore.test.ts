import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { act } from '@testing-library/react';
import { useBossStore, __resetBossStoreForTests, BossResultPayload } from './bossStore';

describe('bossStore', () => {
    beforeEach(() => {
        vi.useFakeTimers();
        __resetBossStoreForTests();
    });

    afterEach(() => {
        vi.clearAllTimers();
        vi.useRealTimers();
    });

    it('starts a boss with correct initial state', () => {
        act(() => {
            useBossStore.getState().startBoss({
                bossId: 'boss-reactor-core',
                name: 'Reactor Core Meltdown',
                difficulty: 'normal',
                durationSeconds: 30 * 60,
                hpPenaltyOnFail: 10,
                baseXpReward: 300,
            });
        });

        const state = useBossStore.getState();
        expect(state.activeBossId).toBe('boss-reactor-core');
        expect(state.status).toBe('active');
        expect(state.deadlineTs).toBeTruthy();
        expect(state.integrityCurrent).toBe(100);
    });

    it('applies boss result and marks defeated on pass', () => {
        act(() => {
            useBossStore.getState().startBoss({
                bossId: 'boss-reactor-core',
                name: 'Reactor Core Meltdown',
                difficulty: 'normal',
                durationSeconds: 60,
                hpPenaltyOnFail: 10,
                baseXpReward: 300,
            });
        });

        const result: BossResultPayload = {
            boss_id: 'boss-reactor-core',
            passed: true,
            score: 92,
            integrity_delta: +5,
            xp_awarded: 300,
            breakdown: { async: 40, model: 30, structure: 20, style: 10 },
        };

        act(() => {
            useBossStore.getState().applyBossResult(result);
        });

        const state = useBossStore.getState();
        expect(state.status).toBe('defeated');
        expect(state.integrityCurrent).toBe(100); // 100 + 5, clamped to max 100
        expect(state.activeBossId).toBeNull();
        expect(state.lastResult?.score).toBe(92);
    });

    it('applies boss result and marks failed on fail', () => {
        act(() => {
            useBossStore.getState().startBoss({
                bossId: 'boss-reactor-core',
                name: 'Reactor Core Meltdown',
                difficulty: 'normal',
                durationSeconds: 60,
                hpPenaltyOnFail: 10,
                baseXpReward: 300,
            });
        });

        const result: BossResultPayload = {
            boss_id: 'boss-reactor-core',
            passed: false,
            score: 40,
            integrity_delta: -20,
            xp_awarded: 0,
            breakdown: { async: 15, model: 10, structure: 10, style: 5 },
        };

        act(() => {
            useBossStore.getState().applyBossResult(result);
        });

        const state = useBossStore.getState();
        expect(state.status).toBe('failed');
        expect(state.integrityCurrent).toBe(80); // 100 - 20
        expect(state.activeBossId).toBeNull();
    });

    it('times out and marks boss as failed when timeout is called', () => {
        act(() => {
            useBossStore.getState().startBoss({
                bossId: 'boss-reactor-core',
                name: 'Reactor Core Meltdown',
                difficulty: 'normal',
                durationSeconds: 3,
                hpPenaltyOnFail: 10,
                baseXpReward: 300,
            });
        });

        // Manually trigger timeout (BossHud does this when deadline hits)
        act(() => {
            useBossStore.getState().timeoutBoss();
        });

        const state = useBossStore.getState();
        expect(state.status).toBe('failed');
        expect(state.activeBossId).toBeNull();
        expect(state.integrityCurrent).toBe(90); // 100 - 10 timeout penalty
    });

    it('does not timeout if boss is not active', () => {
        // Don't start a boss
        act(() => {
            useBossStore.getState().timeoutBoss();
        });

        const state = useBossStore.getState();
        expect(state.status).toBe('idle');
        expect(state.integrityCurrent).toBe(100); // No penalty
    });
});
