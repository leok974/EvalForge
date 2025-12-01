import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
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

// Mock Child Components to reduce noise
vi.mock('../../components/Scoreboard', () => ({ Scoreboard: () => <div>Scoreboard</div> }));
vi.mock('../../components/ContextSelector', () => ({ ContextSelector: () => <div>Selector</div> }));

describe('DevUI NPC Rendering', () => {
    beforeEach(() => {
        vi.resetAllMocks();
        (AuthHook.useAuth as any).mockReturnValue({ user: { id: 'leo' } });
        // Mock scrollIntoView
        window.HTMLElement.prototype.scrollIntoView = vi.fn();
    });

    it('renders standard assistant message (No NPC)', () => {
        (StreamHook.useArcadeStream as any).mockReturnValue({
            messages: [{ role: 'assistant', content: 'Hello standard.' }],
            isStreaming: false,
            sendMessage: vi.fn()
        });

        render(<DevUI />);
        expect(screen.getByText('Hello standard.')).toBeDefined();
        // Should NOT find any NPC header elements
        expect(screen.queryByText(/\/\//)).toBeNull();
    });

    it('renders KAI (Quest) Comm Link', () => {
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

        render(<DevUI />);

        // Check Header Text
        expect(screen.getByText('KAI')).toBeDefined();
        expect(screen.getByText('// Mission Control')).toBeDefined();

        // Check Content
        expect(screen.getByText('Mission Start.')).toBeDefined();

        // Check Styling (Cyan) via class presence
        const header = screen.getByText('KAI');
        expect(header.className).toContain('text-cyan-400');
    });

    it('renders ZERO (Judge) Comm Link', () => {
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

        render(<DevUI />);

        // Check Red Styling
        const header = screen.getByText('ZERO');
        expect(header.className).toContain('text-red-500');
    });
});
