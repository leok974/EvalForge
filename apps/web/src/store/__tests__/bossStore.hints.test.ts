import { describe, it, expect, beforeEach } from 'vitest';
import { useBossStore } from '../bossStore';

describe('Boss Hint System', () => {
    beforeEach(() => {
        // Reset store before each test - set to initial state
        useBossStore.setState({
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
        });
    });

    it('should initialize with no hint', () => {
        const { hintCodexId, hintUnread } = useBossStore.getState();
        expect(hintCodexId).toBeNull();
        expect(hintUnread).toBe(false);
    });

    it('should unlock hint when boss result includes hint_codex_id', () => {
        const store = useBossStore.getState();

        store.applyBossResult({
            boss_id: 'boss-reactor-core',
            score: 45,
            passed: false,
            breakdown: {},
            xp_awarded: 0,
            integrity_delta: -10,
            hint_codex_id: 'boss-reactor-core',
            fail_streak: 2,
        });

        const { hintCodexId, hintUnread } = useBossStore.getState();
        expect(hintCodexId).toBe('boss-reactor-core');
        expect(hintUnread).toBe(true);
    });

    it('should not unlock hint on first failure', () => {
        const store = useBossStore.getState();

        store.applyBossResult({
            boss_id: 'boss-reactor-core',
            score: 50,
            passed: false,
            breakdown: {},
            xp_awarded: 0,
            integrity_delta: -10,
            fail_streak: 1,
        });

        const { hintCodexId, hintUnread } = useBossStore.getState();
        expect(hintCodexId).toBeNull();
        expect(hintUnread).toBe(false);
    });

    it('should mark hint as read', () => {
        const store = useBossStore.getState();

        // Unlock hint first
        store.unlockHint('boss-reactor-core');
        expect(useBossStore.getState().hintUnread).toBe(true);

        // Mark as read
        store.markHintRead();

        const { hintCodexId, hintUnread } = useBossStore.getState();
        expect(hintCodexId).toBe('boss-reactor-core'); // Still available
        expect(hintUnread).toBe(false); // But marked as read
    });

    it('should clear hint on new boss start', () => {
        const store = useBossStore.getState();

        // Unlock hint
        store.unlockHint('boss-reactor-core');
        expect(useBossStore.getState().hintCodexId).toBe('boss-reactor-core');

        // Start new boss
        store.startBoss({
            bossId: 'boss-new',
            name: 'New Boss',
            difficulty: 'normal',
            durationSeconds: 1800,
            hpPenaltyOnFail: 10,
            baseXpReward: 300,
        });

        const { hintCodexId, hintUnread } = useBossStore.getState();
        expect(hintCodexId).toBeNull();
        expect(hintUnread).toBe(false);
    });

    it('should handle unlockHint action directly', () => {
        const store = useBossStore.getState();

        store.unlockHint('boss-reactor-core');

        const { hintCodexId, hintUnread } = useBossStore.getState();
        expect(hintCodexId).toBe('boss-reactor-core');
        expect(hintUnread).toBe(true);
    });

    it('should preserve hint_codex_id when marking as read', () => {
        const store = useBossStore.getState();

        store.unlockHint('boss-reactor-core');
        const initialId = useBossStore.getState().hintCodexId;

        store.markHintRead();
        const afterReadId = useBossStore.getState().hintCodexId;

        expect(initialId).toBe(afterReadId);
        expect(afterReadId).toBe('boss-reactor-core');
    });
});
