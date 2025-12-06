import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import DevUI from '../DevUI';
import * as StreamHook from '../../hooks/useArcadeStream';
import * as AuthHook from '../../hooks/useAuth';

// Mock Hooks
vi.mock('../../hooks/useArcadeStream', () => ({
    useArcadeStream: vi.fn()
}));
vi.mock('../../hooks/useAuth', () => ({
    useAuth: vi.fn()
}));

// Mock Fetch
global.fetch = vi.fn();

// Mock useSkills
vi.mock('../../hooks/useSkills', () => ({
    useSkills: () => ({
        hasSkill: () => true,
        godMode: false
    })
}));

import { createMockBossStoreState } from '../../test/mockBossStore';
const bossStoreState = createMockBossStoreState();
vi.mock('../../store/bossStore', () => ({
    useBossStore: (selector?: any) => selector ? selector(bossStoreState) : bossStoreState
}));

// Mock Child Components to reduce noise
vi.mock('../../components/Scoreboard', () => ({ Scoreboard: () => <div>Scoreboard</div> }));
vi.mock('../../components/ContextSelector', () => ({ ContextSelector: () => <div>Selector</div> }));

describe('DevUI NPC Rendering', () => {
    beforeEach(() => {
        vi.resetAllMocks();
        (AuthHook.useAuth as any).mockReturnValue({ user: { id: 'leo' }, loading: false });

        // Mock fetch to return empty session
        (global.fetch as any).mockImplementation((url: string) => {
            if (url.includes('/api/boss/history')) {
                return Promise.resolve({
                    ok: true,
                    json: async () => []
                });
            }
            if (url.includes('/api/practice_rounds/today')) {
                return Promise.resolve({
                    ok: true,
                    json: async () => ({ items: [] })
                });
            }
            if (url.includes('/api/quests')) {
                return Promise.resolve({
                    ok: true,
                    json: async () => []
                });
            }
            return Promise.resolve({
                ok: true,
                json: async () => ({})
            });
        });

        // Mock scrollIntoView
        window.HTMLElement.prototype.scrollIntoView = vi.fn();
    });

    // ... (existing imports)

    it('renders standard assistant message (No NPC)', async () => {
        (StreamHook.useArcadeStream as any).mockReturnValue({
            messages: [{ role: 'assistant', content: 'Hello standard.' }],
            isStreaming: false,
            sendMessage: vi.fn()
        });

        render(
            <MemoryRouter>
                <DevUI />
            </MemoryRouter>
        );

        // Open Terminal
        fireEvent.click(screen.getByText('Terminal'));

        expect(await screen.findByText('Hello standard.')).toBeDefined();
        // Should NOT find any NPC header elements
        expect(screen.queryByText(/\/\//)).toBeNull();
    });

    it('renders KAI (Quest) Comm Link', async () => {
        (StreamHook.useArcadeStream as any).mockReturnValue({
            messages: [{
                role: 'assistant',
                content: 'Mission Start.',
                npc: {
                    id: 'npc_kai',
                    name: 'KAI',
                    title: 'Mission Control',
                    color: 'cyan',
                    avatar_icon: 'radar'
                }
            }],
            isStreaming: false,
            sendMessage: vi.fn()
        });

        render(
            <MemoryRouter>
                <DevUI />
            </MemoryRouter>
        );

        // Open Terminal
        fireEvent.click(screen.getByText('Terminal'));

        // Check Header Text
        expect(await screen.findByText('KAI')).toBeDefined();
        expect(screen.getByText('// Mission Control')).toBeDefined();

        // Check Content
        expect(screen.getByText('Mission Start.')).toBeDefined();

        // Check Styling (Cyan) via class presence
        const header = screen.getByText('KAI');
        expect(header.className).toContain('text-cyan-400');
    });

    it('renders ZERO (Judge) Comm Link', async () => {
        (StreamHook.useArcadeStream as any).mockReturnValue({
            messages: [{
                role: 'assistant',
                content: 'Compliance Failure.',
                npc: {
                    id: 'npc_zero',
                    name: 'ZERO',
                    title: 'Arbiter',
                    color: 'red',
                    avatar_icon: 'eye'
                }
            }],
            isStreaming: false,
            sendMessage: vi.fn()
        });

        render(
            <MemoryRouter>
                <DevUI />
            </MemoryRouter>
        );

        // Open Terminal
        fireEvent.click(screen.getByText('Terminal'));

        // Check Red Styling
        const header = await screen.findByText('ZERO');
        expect(header.className).toContain('text-red-500');
    });
});
