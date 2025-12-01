import React from 'react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BossHistoryPanel } from '../BossHistoryPanel';

describe('BossHistoryPanel', () => {
    const originalFetch = global.fetch;

    beforeEach(() => {
        // @ts-expect-error – we will stub fetch for tests
        global.fetch = vi.fn();
    });

    afterEach(() => {
        global.fetch = originalFetch;
        vi.restoreAllMocks();
    });

    it('renders raid stats and recent runs', async () => {
        const runs = [
            {
                boss_id: 'reactor_core',
                boss_name: 'Reactor Core Meltdown',
                difficulty: 'hard',
                score: 95,
                passed: true,
                integrity_delta: 10,
                xp_awarded: 600,
                created_at: '2025-01-02T12:00:00Z',
            },
            {
                boss_id: 'reactor_core',
                boss_name: 'Reactor Core Meltdown',
                difficulty: 'normal',
                score: 80,
                passed: false,
                integrity_delta: -20,
                xp_awarded: 0,
                created_at: '2025-01-01T10:00:00Z',
            },
        ];

        // @ts-expect-error – mocked
        global.fetch.mockResolvedValue({
            ok: true,
            json: async () => runs,
        });

        render(<BossHistoryPanel />);

        // Wait for loading to complete
        await waitFor(() =>
            expect(screen.queryByText(/Loading/i)).toBeFalsy()
        );

        // Header stats
        expect(screen.getByText(/1\/2 cleared/i)).toBeTruthy();
        expect(screen.getByText(/Best 95/i)).toBeTruthy();

        // Individual rows - use getAllByText since "Reactor Core Meltdown" appears twice
        expect(screen.getAllByText(/Reactor Core Meltdown/)).toHaveLength(2);
        expect(screen.getByText(/Score 95/)).toBeTruthy();
        expect(screen.getByText(/Score 80/)).toBeTruthy();
    });

    it('shows empty-state hint when there are no runs', async () => {
        // @ts-expect-error – mocked
        global.fetch.mockResolvedValue({
            ok: true,
            json: async () => [],
        });

        render(<BossHistoryPanel />);

        await waitFor(() =>
            expect(screen.queryByText(/Loading/i)).toBeFalsy()
        );

        expect(screen.getByText(/No raids logged yet/i)).toBeTruthy();
    });

    it('handles fetch errors gracefully', async () => {
        // @ts-expect-error – mocked
        global.fetch.mockRejectedValue(new Error('Network error'));

        render(<BossHistoryPanel />);

        await waitFor(() =>
            expect(screen.queryByText(/Loading/i)).toBeFalsy()
        );

        // Should show empty state on error
        expect(screen.getByText(/No raids logged yet/i)).toBeTruthy();
    });
});
