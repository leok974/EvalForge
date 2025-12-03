import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { CodexDrawer } from '../CodexDrawer';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import * as bossApi from '../../lib/bossCodexApi';

// Mock the APIs
vi.mock('../../lib/bossCodexApi', () => ({
    fetchBossList: vi.fn(),
    fetchBossBundle: vi.fn(),
}));

vi.mock('../../lib/projectCodexApi', () => ({
    getProjectCodexProjects: vi.fn().mockResolvedValue([]),
    getProjectCodexBundle: vi.fn(),
}));

// Mock fetch for system codex
global.fetch = vi.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve([]),
    })
) as any;

describe('CodexDrawer - Boss Tab', () => {
    const mockBossList = [
        {
            boss_id: 'reactor_core',
            name: 'The Reactor Core',
            world_id: 'world-python',
            tier_unlocked: 2,
            kills: 0,
            deaths: 3,
            docs: [
                { slug: 'boss-reactor-core-lore', title: 'Lore', tier: 1 },
                { slug: 'boss-reactor-core-attacks', title: 'Attacks', tier: 2 },
                { slug: 'boss-reactor-core-strategy', title: 'Strategy', tier: 3 },
            ],
        },
    ];

    const mockBossBundle = {
        boss: {
            boss_id: 'reactor_core',
            name: 'The Reactor Core',
            world_id: 'world-python',
            tier_unlocked: 2,
        },
        docs: [
            { slug: 'boss-reactor-core-lore', title: 'Lore', tier: 1, unlocked: true, body_md: '# Lore Content' },
            { slug: 'boss-reactor-core-attacks', title: 'Attacks', tier: 2, unlocked: true, body_md: '# Attacks Content' },
            { slug: 'boss-reactor-core-strategy', title: 'Strategy', tier: 3, unlocked: false, body_md: null },
        ],
    };

    beforeEach(() => {
        vi.clearAllMocks();
        (bossApi.fetchBossList as any).mockResolvedValue(mockBossList);
        (bossApi.fetchBossBundle as any).mockResolvedValue(mockBossBundle);
    });

    it('renders boss list and respects unlocked flags', async () => {
        render(<CodexDrawer isOpen={true} onClose={() => { }} currentWorldId="world-python" />);

        // Switch to Boss Tab
        const bossTab = screen.getByText(/boss intel/i);
        fireEvent.click(bossTab);

        // Wait for boss list to load
        await waitFor(() => {
            expect(bossApi.fetchBossList).toHaveBeenCalled();
        });

        // Wait for boss list to appear
        const bossItem = await screen.findByTestId('boss-item-reactor_core');
        expect(bossItem).toBeTruthy();

        // Check list item details
        expect(screen.getByText('Tier 2/3')).toBeTruthy();

        // Click the boss to load details
        fireEvent.click(bossItem);

        // Wait for bundle to load
        expect(await screen.findByText(/BOSS INTEL – THE REACTOR CORE/i)).toBeTruthy();

        // Check unlocked docs
        expect(screen.getByText('TIER 1 – Lore')).toBeTruthy();
        expect(screen.getByText('Lore Content')).toBeTruthy();

        // Check locked doc
        expect(screen.getByText('TIER 3 – Strategy')).toBeTruthy();
        expect(screen.getByText('LOCKED')).toBeTruthy();
        expect(screen.getByText('REDACTED.')).toBeTruthy();
        expect(screen.queryByText('Strategy Content')).toBeNull();
    });
});
