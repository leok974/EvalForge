import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { EventLog } from '../EventLog';
import * as HookModule from '../../../hooks/useGameSocket';

// Mock the socket hook
vi.mock('../../../hooks/useGameSocket', () => ({
    useGameSocket: vi.fn()
}));

describe('EventLog Component', () => {
    beforeEach(() => {
        vi.useFakeTimers();
        // Default: No event
        (HookModule.useGameSocket as any).mockReturnValue(null);
    });

    afterEach(() => {
        vi.useRealTimers();
        vi.resetAllMocks();
    });

    it('renders boot sequence on mount', () => {
        render(<EventLog />);

        // Check initial boot message
        expect(screen.getByText(/System Boot Sequence/i)).toBeDefined();

        // Check delayed connection message
        act(() => {
            vi.advanceTimersByTime(600);
        });
        expect(screen.getByText(/Connected to EvalForge/i)).toBeDefined();
    });

    it('logs Boss Spawn events', () => {
        const { rerender } = render(<EventLog />);

        // Simulate Boss Event
        (HookModule.useGameSocket as any).mockReturnValue({
            type: 'boss_spawn',
            title: 'MEGA BUG DETECTED'
        });

        // Rerender to trigger useEffect
        rerender(<EventLog />);

        const logEntry = screen.getByText(/WARNING: MEGA BUG DETECTED/i);
        expect(logEntry).toBeDefined();
        // Check styling (rose color for boss warnings) - verifying class presence
        expect(logEntry.className).toContain('text-rose-400');
    });

    it('logs Sync Complete events', () => {
        const { rerender } = render(<EventLog />);

        (HookModule.useGameSocket as any).mockReturnValue({
            type: 'sync_complete',
            title: 'REPO INDEXED'
        });

        rerender(<EventLog />);

        const logEntry = screen.getByText(/SUCCESS: REPO INDEXED/i);
        expect(logEntry).toBeDefined();
        // Check styling (green/emerald)
        expect(logEntry.className).toContain('text-emerald-400');
    });
});
