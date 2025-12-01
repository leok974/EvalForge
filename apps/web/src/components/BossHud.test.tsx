import React from 'react';
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BossHud } from './BossHud';
import { useBossStore, __resetBossStoreForTests, BossResultPayload } from '../store/bossStore';
import { act } from '@testing-library/react';

function renderHud() {
    return render(<BossHud />);
}

describe('BossHud', () => {
    beforeEach(() => {
        __resetBossStoreForTests();
    });

    it('does not render when there is no active boss', () => {
        renderHud();
        // HUD should be completely hidden when idle
        const bossText = screen.queryByText(/boss/i);
        expect(bossText).toBeNull();
    });

    it('renders HUD when boss is active', () => {
        act(() => {
            useBossStore.getState().startBoss({
                bossId: 'boss-reactor-core',
                name: 'Reactor Core Meltdown',
                difficulty: 'normal',
                durationSeconds: 1800,
                hpPenaltyOnFail: 10,
                baseXpReward: 300,
            });
        });

        renderHud();

        // Check for boss-specific text
        expect(screen.getByText(/reactor core meltdown/i)).toBeTruthy();
        expect(screen.getByText(/system integrity/i)).toBeTruthy();
    });

    it('shows defeated state when boss is defeated', () => {
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
            score: 95,
            integrity_delta: +10,
            xp_awarded: 400,
            breakdown: { async: 40, model: 35, structure: 20, style: 10 },
        };

        act(() => {
            useBossStore.getState().applyBossResult(result);
        });

        renderHud();

        // Check for "DEFEATED" status text
        expect(screen.getByText(/defeated/i)).toBeTruthy();
        // Score should be displayed
        expect(screen.getByText('95')).toBeTruthy();
    });

    it('shows failure state when boss is failed', () => {
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
            score: 20,
            integrity_delta: -30,
            xp_awarded: 0,
            breakdown: { async: 5, model: 5, structure: 5, style: 5 },
        };

        act(() => {
            useBossStore.getState().applyBossResult(result);
        });

        renderHud();

        // The HUD shows "FAILED" status, not "boss escaped"
        expect(screen.getByText(/failed/i)).toBeTruthy();
        // Score should be displayed
        expect(screen.getByText('20')).toBeTruthy();
    });

    it('displays HP bar with correct percentage', () => {
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

        renderHud();

        // Check that HP values are rendered
        expect(screen.getByText(/100\/100/)).toBeTruthy();
    });
});
