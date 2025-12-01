import { describe, it, expect, beforeEach } from 'vitest';
import { act } from '@testing-library/react';
import { useBossStore, __resetBossStoreForTests } from '../bossStore';

describe('bossStore – difficulty + outcomes', () => {
    beforeEach(() => {
        __resetBossStoreForTests();
    });

    it('startBoss sets boss metadata, difficulty and timer', () => {
        act(() => {
            useBossStore.getState().startBoss({
                bossId: 'reactor_core',
                name: 'Reactor Core Meltdown',
                difficulty: 'hard',
                durationSeconds: 900,
                hpPenaltyOnFail: 20,
                baseXpReward: 600,
            });
        });

        const state = useBossStore.getState();
        expect(state.activeBossId).toBe('reactor_core');
        expect(state.bossName).toBe('Reactor Core Meltdown');
        expect(state.difficulty).toBe('hard');
        expect(state.deadlineTs).toBeTruthy();
        expect(state.status).toBe('active');
    });

    it('applyBossResult updates HP, status and clears active boss when ids match', () => {
        // Arrange: spawn boss -> default hp 100
        act(() => {
            useBossStore.getState().startBoss({
                bossId: 'reactor_core',
                name: 'Reactor Core Meltdown',
                difficulty: 'normal',
                durationSeconds: 600,
                hpPenaltyOnFail: 10,
                baseXpReward: 300,
            });
        });

        // Act: apply a failing result with -20 integrity
        act(() => {
            useBossStore.getState().applyBossResult({
                boss_id: 'reactor_core',
                passed: false,
                score: 42,
                integrity_delta: -20,
                xp_awarded: 0,
                breakdown: {},
            });
        });

        const state = useBossStore.getState();
        expect(state.status).toBe('failed');
        expect(state.integrityCurrent).toBe(80); // 100 - 20
        expect(state.lastResult?.score).toBe(42);
        expect(state.lastResult?.passed).toBe(false);
        expect(state.activeBossId).toBeNull();
    });

    it('applyBossResult clamps HP to valid range', () => {
        act(() => {
            useBossStore.getState().startBoss({
                bossId: 'reactor_core',
                name: 'Reactor Core Meltdown',
                difficulty: 'normal',
                durationSeconds: 600,
                hpPenaltyOnFail: 10,
                baseXpReward: 300,
            });
        });

        // Apply massive damage
        act(() => {
            useBossStore.getState().applyBossResult({
                boss_id: 'reactor_core',
                passed: false,
                score: 10,
                integrity_delta: -150,
                xp_awarded: 0,
                breakdown: {},
            });
        });

        const state = useBossStore.getState();
        expect(state.integrityCurrent).toBe(0); // Clamped to 0, not negative
    });

    it('applies positive HP delta correctly', () => {
        // Start with reduced HP
        act(() => {
            useBossStore.setState({ integrityCurrent: 60 });
            useBossStore.getState().startBoss({
                bossId: 'reactor_core',
                name: 'Reactor Core Meltdown',
                difficulty: 'hard',
                durationSeconds: 600,
                hpPenaltyOnFail: 20,
                baseXpReward: 600,
            });
        });

        // Win with HP restore
        act(() => {
            useBossStore.getState().applyBossResult({
                boss_id: 'reactor_core',
                passed: true,
                score: 95,
                integrity_delta: +15,
                xp_awarded: 600,
                breakdown: {},
            });
        });

        const state = useBossStore.getState();
        expect(state.status).toBe('defeated');
        expect(state.integrityCurrent).toBe(75); // 60 + 15
    });
});
