import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import DevUI from '../DevUI';
import * as AuthHook from '../../hooks/useAuth';
import * as BossStore from '../../store/bossStore';
import { MemoryRouter } from 'react-router-dom';

// --- MOCKS ---
// --- MOCKS ---
global.fetch = vi.fn((url: string) => {
    if (url.includes('/api/boss/history') || url.includes('/api/projects')) {
        return Promise.resolve({
            ok: true,
            json: async () => []
        });
    }
    return Promise.resolve({
        ok: true,
        json: async () => ({})
    });
}) as any;

// Mock Auth to simulate logged-in user
vi.mock('../../hooks/useAuth', () => ({
    useAuth: vi.fn()
}));

// Mock Stream Hook to capture setMessages calls
const mockSetMessages = vi.fn();
vi.mock('../../hooks/useArcadeStream', () => ({
    useArcadeStream: () => ({
        messages: [],
        setMessages: mockSetMessages, // <--- We spy on this
        latestGrade: null,
        isStreaming: false,
        sendMessage: vi.fn()
    })
}));

// Mock Child Components to verify props passed to them
vi.mock('../../components/ContextSelector', () => ({
    ContextSelector: ({ context }: any) => (
        <div data-testid="ctx-display">
            {context.world_id} / {context.track_id} / {context.mode}
        </div>
    )
}));

// Mock Scoreboard to avoid rendering issues
vi.mock('../../components/Scoreboard', () => ({ Scoreboard: () => <div>Scoreboard</div> }));

// Mock useSkills hook
vi.mock('../../hooks/useSkills', () => ({
    useSkills: () => ({
        hasSkill: vi.fn().mockReturnValue(true)
    })
}));

import { createMockBossStoreState } from '../../test/mockBossStore';

// Mock Boss Store
const bossStoreState = createMockBossStoreState({
    runs: [
        { id: '1', boss_slug: 'reactor-core', score: 90, grade: 'S', passed: true, timestamp: Date.now() },
        { id: '2', boss_slug: 'intent-oracle', score: 45, grade: 'F', passed: false, timestamp: Date.now() }
    ]
});

vi.mock('../../store/bossStore', () => ({
    useBossStore: (selector?: any) => selector ? selector(bossStoreState) : bossStoreState
}));

describe('DevUI Session Restoration', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        Element.prototype.scrollIntoView = vi.fn();
    });

    it('fetches active session on mount if user is logged in', async () => {
        // 1. Setup Auth
        (AuthHook.useAuth as any).mockReturnValue({ user: { id: 'leo' } });

        // 2. Setup API Response
        const mockSession = {
            id: 'sess_123',
            world_id: 'world-infra',
            track_id: 'siteagent-infra',
            mode: 'explain',
            history: [{ role: 'user', content: 'Restore this' }]
        };

        (global.fetch as any).mockImplementation((url: string) => {
            if (url.includes('/api/session/active')) {
                return Promise.resolve({
                    ok: true,
                    json: async () => mockSession
                });
            }
            // Fallback for boss/history etc provided by global mock or default
            if (url.includes('/api/boss/history') || url.includes('/api/projects') || url.includes('/api/quests')) {
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
            return Promise.resolve({ ok: true, json: async () => ({}) });
        });

        render(
            <MemoryRouter>
                <DevUI />
            </MemoryRouter>
        );

        // 3. Verify API Call
        expect(global.fetch).toHaveBeenCalledWith('/api/session/active');

        // 4. Verify Context Restoration (via mocked child prop)
        await waitFor(() => {
            const display = screen.getByTestId('ctx-display');
            expect(display.textContent).toContain('world-infra');
            expect(display.textContent).toContain('siteagent-infra');
            expect(display.textContent).toContain('explain');
        });

        // 5. Verify History Restoration
        expect(mockSetMessages).toHaveBeenCalledWith(mockSession.history);
    });

    it('does not fetch session if user is logged out', () => {
        // 1. Setup Guest User
        (AuthHook.useAuth as any).mockReturnValue({ user: null });

        render(
            <MemoryRouter>
                <DevUI />
            </MemoryRouter>
        );

        // 2. Verify No API Call
        expect(global.fetch).not.toHaveBeenCalledWith('/api/session/active');
    });

    it('handles session not found gracefully', async () => {
        (AuthHook.useAuth as any).mockReturnValue({ user: { id: 'leo' } });

        // 2. Return Empty/Null Response
        // 2. Return Empty/Null Response
        (global.fetch as any).mockImplementation((url: string) => {
            if (url.includes('/api/session/active')) {
                return Promise.resolve({
                    ok: true,
                    json: async () => null
                });
            }
            if (url.includes('/api/boss/history') || url.includes('/api/projects')) {
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
            return Promise.resolve({ ok: true, json: async () => ({}) });
        });

        render(
            <MemoryRouter>
                <DevUI />
            </MemoryRouter>
        );

        // Should not crash, should simply not call setMessages
        await waitFor(() => expect(global.fetch).toHaveBeenCalled());
        expect(mockSetMessages).not.toHaveBeenCalled();
    });
});
