import { describe, it, expect, vi, beforeEach, beforeAll, afterEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useSkills } from '../useSkills';

const mockTree = {
    skill_points: 5,
    nodes: [
        { id: 's1', feature_key: 'syntax_highlighting', is_unlocked: true, can_unlock: false },
        { id: 's2', feature_key: 'agent_elara', is_unlocked: false, can_unlock: true }
    ]
};

describe('useSkills Hook', () => {
    beforeAll(() => {
        // Verify god mode is OFF in tests
        console.log('🔍 ENV in useSkills.test.ts', {
            DEV_UNLOCK: import.meta.env.VITE_DEV_UNLOCK_ALL,
            UNLOCK_ALL: import.meta.env.VITE_UNLOCK_ALL,
            LAYOUT_UNLOCK: import.meta.env.VITE_LAYOUT_UNLOCK_ALL,
        });

        global.fetch = vi.fn();
        window.fetch = global.fetch;
    });

    afterEach(() => {
        vi.clearAllMocks();
    });

    it('fetches tree on mount', async () => {
        console.log("Setting up mock for fetch");
        (fetch as any).mockImplementation(() => {
            console.log("Fetch called!");
            return Promise.resolve({
                ok: true,
                json: async () => {
                    console.log("JSON called!");
                    return mockTree;
                }
            });
        });

        const user = { id: 'leo' }; // Stable reference
        const { result } = renderHook(() => useSkills(user));

        expect(result.current.loading).toBe(true);

        await waitFor(() => {
            if (result.current.loading) console.log("Still loading...");
            expect(result.current.loading).toBe(false);
        });

        expect(result.current.skillPoints).toBe(5);
        expect(result.current.skills).toHaveLength(2);
    });

    it('hasSkill returns correct state', async () => {
        (fetch as any).mockResolvedValue({
            ok: true,
            json: async () => mockTree
        });

        const user = { id: 'leo' };
        const { result } = renderHook(() => useSkills(user));
        await waitFor(() => expect(result.current.loading).toBe(false));

        // Check unlocked
        expect(result.current.hasSkill('syntax_highlighting')).toBe(true);
        // Check locked
        expect(result.current.hasSkill('agent_elara')).toBe(false);
        // Check missing
        expect(result.current.hasSkill('unknown_feature')).toBe(false);
    });

    it('unlockSkill triggers refresh on success', async () => {
        // 1. Initial Load
        (fetch as any).mockResolvedValueOnce({
            ok: true,
            json: async () => mockTree
        });

        const user = { id: 'leo' };
        const { result } = renderHook(() => useSkills(user));
        await waitFor(() => expect(result.current.loading).toBe(false));

        // 2. Setup Unlock Mock (Success)
        (fetch as any).mockResolvedValueOnce({
            ok: true,
            json: async () => ({ status: 'ok' })
        });

        // 3. Setup Refresh Mock (Called after unlock)
        (fetch as any).mockResolvedValueOnce({
            ok: true,
            json: async () => ({ ...mockTree, skill_points: 4 }) // Simulating change
        });

        await result.current.unlockSkill('s2');

        expect(fetch).toHaveBeenCalledTimes(3); // Init, Post, Refresh
    });
});
