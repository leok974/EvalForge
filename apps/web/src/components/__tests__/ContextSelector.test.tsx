import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ContextSelector } from '../ContextSelector';
import React from 'react';

// Mock Fetch
global.fetch = vi.fn();

const mockUniverse = {
    worlds: [
        { id: 'w1', name: 'World 1', icon: '🌍' }
    ],
    tracks: [
        { id: 't1', name: 'Track 1', world_id: 'w1', source: 'personal' },
        { id: 't2', name: 'Track 2', world_id: 'w1', source: 'fundamentals' }
    ]
};

describe('ContextSelector', () => {
    beforeEach(() => {
        (global.fetch as any).mockResolvedValue({
            json: async () => mockUniverse,
        });
    });

    it('renders worlds and groups tracks', async () => {
        const setContext = vi.fn();
        const hasSkill = vi.fn().mockReturnValue(true);
        render(<ContextSelector context={{ mode: 'judge', world_id: 'w1', track_id: '' }} setContext={setContext} hasSkill={hasSkill} />);

        // Wait for fetch
        await waitFor(() => screen.getByText(/World 1/i));

        // Check Groups
        expect(screen.getByRole('group', { name: 'My Projects (BYOR)' })).toBeDefined();
        expect(screen.getByRole('group', { name: 'Fundamentals' })).toBeDefined();
    });

    it('updates context on selection', async () => {
        const setContext = vi.fn();
        const hasSkill = vi.fn().mockReturnValue(true);
        render(<ContextSelector context={{ mode: 'judge', world_id: 'w1', track_id: '' }} setContext={setContext} hasSkill={hasSkill} />);

        await waitFor(() => screen.getByText(/World 1/i));

        // Select Track 1
        // Note: Since we have multiple selects, we target by role and filter or use specific selectors
        // For simplicity in this test, we assume the second combobox is the track selector
        const selects = screen.getAllByRole('combobox');
        fireEvent.change(selects[1], { target: { value: 't1' } });

        expect(setContext).toHaveBeenCalled();
    });
});
