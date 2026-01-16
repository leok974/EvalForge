import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import React from "react";
// Mock react-router-dom
const navigate = vi.fn();
vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual('react-router-dom');
    return {
        ...actual,
        useNavigate: () => navigate,
        useLocation: () => ({ pathname: '/arcade' }),
        BrowserRouter: ({ children }: { children: React.ReactNode }) => <div>{children}</div>
    };
});

// Mock hook dependencies
vi.mock('../../hooks/useAuth', () => ({
    useAuth: () => ({
        user: { id: 'test-user', name: 'Test User' },
        login: vi.fn(),
        loading: false
    })
}));

vi.mock('../../hooks/useArcadeStream', () => ({
    useArcadeStream: () => ({
        messages: [],
        setMessages: vi.fn(),
        latestGrade: null,
        isStreaming: false,
        sendMessage: vi.fn()
    }),
    StreamContext: {}
}));

vi.mock('../../hooks/useSkills', () => ({
    useSkills: () => ({
        hasSkill: () => true,
        godMode: false
    })
}));

vi.mock('../../store/bossStore', () => ({
    useBossStore: () => ({ status: 'idle', lastResult: null })
}));

vi.mock('../../store/gameStore', () => ({
    useGameStore: () => ({
        universe: {
            worlds: [
                {
                    slug: 'world-python',
                    tracks: [{ slug: 'applylens-backend' }]
                }
            ]
        }
    })
}));

vi.mock('../../hooks/useTrackWarp', () => ({
    useTrackWarp: () => { }
}));

vi.mock('../../hooks/useCurrentLayout', () => ({
    useCurrentLayout: () => ({ layout: 'workshop' }),
    LayoutProvider: ({ children }: any) => <div>{children}</div>
}));

// Mock Child Components
vi.mock('../../components/QuestBoard', () => ({
    QuestBoard: ({ onOpenQuest }: { onOpenQuest: (q: any) => void }) => (
        <div data-testid="quest-board-mock">
            <button
                data-testid="start-quest-btn"
                onClick={() => onOpenQuest({
                    id: 100,
                    slug: 'py-ignition-q1',
                    title: 'Active Quest Title',
                    short_description: 'Active Quest Description',
                    base_xp_reward: 50,
                    state: 'available'
                })}
            >
                Start Quest
            </button>
        </div>
    )
}));

// Import Component under test
import DevUI from "../DevUI";

describe("DevUI Active Quest Header", () => {
    beforeEach(() => {
        vi.clearAllMocks();

        // Mock scrollIntoView
        window.HTMLElement.prototype.scrollIntoView = vi.fn();

        // Mock fetch for profile/me
        global.fetch = vi.fn().mockImplementation((url) => {
            if (url === '/api/profile/me') return Promise.resolve({ ok: true });
            if (url === '/api/session/active') return Promise.resolve({ json: () => Promise.resolve({}) });
            if (url === '/api/universe') return Promise.resolve({
                json: () => Promise.resolve({
                    worlds: [
                        { slug: 'world-python', label: 'Python', tracks: [] }
                    ]
                })
            });
            return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
        });
    });

    it("switch to terminal view and show Active Quest Header when a quest is opened", async () => {
        const { MemoryRouter } = await import('react-router-dom');
        render(
            <MemoryRouter>
                <DevUI />
            </MemoryRouter>
        );

        // 1. Find the mock QuestBoard button and click it to simulate starting a quest
        const startBtn = await screen.findByTestId("start-quest-btn");
        fireEvent.click(startBtn);

        // 2. Expect View to switch to Terminal (QuestBoard mock disappear)
        // Note: The QuestBoard is rendered conditionally viewMode === 'board'.
        // If we switch to 'terminal', QuestBoard should NOT be in document.
        await waitFor(() => {
            expect(screen.queryByTestId("quest-board-mock")).not.toBeInTheDocument();
        });

        // 3. Verify Active Quest Header Content
        // Use exact match regex to avoid matching "Active Quest Title"
        expect(screen.getByText(/^Active Quest\s*$/i)).toBeInTheDocument();
        expect(screen.getByText(/Active Quest Title/i)).toBeInTheDocument();
        expect(screen.getByText(/Active Quest Description/i)).toBeInTheDocument();
        expect(screen.getByText("50")).toBeInTheDocument(); // XP
    });
});
