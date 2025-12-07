import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import DevUI from '../DevUI';
import * as SkillsHook from '../../hooks/useSkills';
import * as AuthHook from '../../hooks/useAuth';
import * as StreamHook from '../../hooks/useArcadeStream';
import * as BossStore from '../../store/bossStore';
import { MemoryRouter } from 'react-router-dom';

// Mock Hooks
vi.mock('../../hooks/useArcadeStream', () => ({
    useArcadeStream: vi.fn()
}));
vi.mock('../../hooks/useAuth', () => ({
    useAuth: vi.fn()
}));
vi.mock('../../hooks/useSkills', () => ({
    useSkills: vi.fn()
}));
vi.mock('../../store/bossStore', () => ({
    useBossStore: vi.fn()
}));
vi.mock('../../store/agentStore', () => ({
    useAgentStore: () => ({ openAgent: vi.fn() })
}));
vi.mock('../../store/gameStore', () => ({
    useGameStore: vi.fn((selector) => {
        const state = {
            layout: 'workshop',
            setLayout: vi.fn(),
            addXp: vi.fn(),
            activeTrack: null
        };
        return selector ? selector(state) : state;
    })
}));

// Mock Child Components
vi.mock('../../components/Scoreboard', () => ({ Scoreboard: () => <div>Scoreboard</div> }));
vi.mock('../../components/ContextSelector', () => ({ ContextSelector: () => <div>Selector</div> }));
vi.mock('../../components/BossPanel', () => ({ BossPanel: () => <div>BossPanel</div> }));
vi.mock('../../components/BossHud', () => ({ BossHud: () => <div data-testid="boss-hud">BossHud</div> }));
vi.mock('../../components/practice/PracticeGauntletCard', () => ({
    PracticeGauntletCard: () => <div data-testid="mock-practice-gauntlet">Mock Gauntlet</div>
}));

describe('DevUI Skill Gating', () => {
    beforeEach(() => {
        vi.clearAllMocks();

        // Robust Fetch Mock
        const fetchMock = vi.fn((url: string | Request | URL) => {
            const urlStr = url.toString();
            if (urlStr.includes('/api/boss/history') || urlStr.includes('/api/projects') || urlStr.includes('/api/quests')) {
                return Promise.resolve({ ok: true, json: async () => [] });
            }
            if (urlStr.includes('/api/session/active')) {
                // Default to empty/no session unless overridden
                return Promise.resolve({ ok: true, json: async () => ({}) });
            }
            return Promise.resolve({ ok: true, json: async () => ({}) });
        });
        vi.stubGlobal('fetch', fetchMock);

        (AuthHook.useAuth as any).mockReturnValue({ user: { id: 'leo' } });
        (StreamHook.useArcadeStream as any).mockReturnValue({
            messages: [],
            isStreaming: false,
            sendMessage: vi.fn()
        });
        (BossStore.useBossStore as any).mockReturnValue({ status: 'idle' });
        // Mock scrollIntoView
        window.HTMLElement.prototype.scrollIntoView = vi.fn();
    });

    it('renders RAW MODE when syntax_highlighter is locked', () => {
        (SkillsHook.useSkills as any).mockReturnValue({
            hasSkill: (key: string) => false // All locked
        });

        render(
            <MemoryRouter>
                <DevUI />
            </MemoryRouter>
        );

        // Switch to Terminal View to see Input
        fireEvent.click(screen.getByText('Terminal'));

        // Editor should show raw mode placeholder
        expect(screen.getByPlaceholderText(/RAW MODE/)).toBeDefined();
        // Agent buttons should be disabled/locked
        expect(screen.getByText(/EXPLAIN 🔒/)).toBeDefined();
        expect(screen.getByText(/DEBUG 🔒/)).toBeDefined();
    });

    it('renders Standard Editor when syntax_highlighter is unlocked', () => {
        (SkillsHook.useSkills as any).mockReturnValue({
            hasSkill: (key: string) => key === 'syntax_highlighter'
        });

        render(
            <MemoryRouter>
                <DevUI />
            </MemoryRouter>
        );

        // Switch to Terminal View
        fireEvent.click(screen.getByText('Terminal'));

        // Editor should show standard placeholder
        expect(screen.getByPlaceholderText(/Paste code or ask a question/)).toBeDefined();
        // Agents still locked
        expect(screen.getByText(/EXPLAIN 🔒/)).toBeDefined();
    });

    it('enables EXPLAIN button when agent_explain is unlocked', () => {
        (SkillsHook.useSkills as any).mockReturnValue({
            hasSkill: (key: string) => key === 'agent_explain'
        });

        render(
            <MemoryRouter>
                <DevUI />
            </MemoryRouter>
        );

        const btn = screen.getByText('EXPLAIN'); // No lock icon
        expect(btn).toBeDefined();
        expect(btn.closest('button')).not.toBeDisabled();

        // DEBUG still locked
        expect(screen.getByText(/DEBUG 🔒/)).toBeDefined();
    });

    it('enables DEBUG button when agent_debug is unlocked', () => {
        (SkillsHook.useSkills as any).mockReturnValue({
            hasSkill: (key: string) => key === 'agent_debug'
        });

        render(
            <MemoryRouter>
                <DevUI />
            </MemoryRouter>
        );

        const btn = screen.getByText('DEBUG'); // No lock icon
        expect(btn).toBeDefined();
        expect(btn.closest('button')).not.toBeDisabled();
    });
});
