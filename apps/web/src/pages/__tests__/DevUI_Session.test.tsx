import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import DevUI from '../DevUI';
import * as AuthHook from '../../hooks/useAuth';
import * as StreamHook from '../../hooks/useArcadeStream';

// --- MOCKS ---
global.fetch = vi.fn();

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

describe('DevUI Session Restoration', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        // Mock scrollIntoView
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

        (global.fetch as any).mockResolvedValueOnce({
            json: async () => mockSession
        });

        render(<DevUI />);

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

        render(<DevUI />);

        // 2. Verify No API Call
        expect(global.fetch).not.toHaveBeenCalledWith('/api/session/active');
    });

    it('handles session not found gracefully', async () => {
        (AuthHook.useAuth as any).mockReturnValue({ user: { id: 'leo' } });

        // 2. Return Empty/Null Response
        (global.fetch as any).mockResolvedValueOnce({
            json: async () => null
        });

        render(<DevUI />);

        // Should not crash, should simply not call setMessages
        await waitFor(() => expect(global.fetch).toHaveBeenCalled());
        expect(mockSetMessages).not.toHaveBeenCalled();
    });
});
