import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import DevUI from "../DevUI";
import { STARTER_QUEST_ROUTE, TUTORIAL_STORAGE_KEY } from "@/config/starter";

// Define spy outside
const mockNavigateSpy = vi.fn();

// --- MOCKS ---
vi.mock("react-router-dom", async () => {
    const actual = await vi.importActual<any>("react-router-dom");
    return {
        ...actual,
        useNavigate: () => mockNavigateSpy,
        useLocation: () => ({ pathname: '/workshop' }),
    };
});

// Mock hooks to avoid crash
vi.mock("@/hooks/useAuth", () => ({ useAuth: () => ({ user: { id: 'test-user' }, loading: false }) }));
vi.mock("@/hooks/useArcadeStream", () => ({ useArcadeStream: () => ({ messages: [], isStreaming: false }) }));
vi.mock("@/hooks/useSkills", () => ({ useSkills: () => ({ hasSkill: () => true, godMode: false }) }));
vi.mock("@/store/bossStore", () => ({ useBossStore: () => ({ status: 'idle' }) }));
vi.mock("@/hooks/useTrackWarp", () => ({ useTrackWarp: () => { } }));
vi.mock("@/hooks/useCurrentLayout", () => ({
    useCurrentLayout: () => ({ layout: 'workshop' }),
    LayoutProvider: ({ children }: any) => <div>{children}</div>
}));
vi.mock("@/store/gameStore", () => ({ useGameStore: () => ({}) }));
vi.mock("@/components/Scoreboard", () => ({ Scoreboard: () => <div>Scoreboard</div> }));
vi.mock("@/components/ContextSelector", () => ({ ContextSelector: () => <div>ContextSelector</div> }));
vi.mock("@/components/BossPanel", () => ({ BossPanel: () => <div>BossPanel</div> }));
vi.mock("@/components/CodexDrawer", () => ({ CodexDrawer: () => <div>CodexDrawer</div> }));
vi.mock("@/components/tracks/OracleTrackCard", () => ({ OracleTrackCard: () => <div>OracleTrackCard</div> }));
vi.mock("@/components/devtools/IntentOracleEvalButton", () => ({ IntentOracleEvalButton: () => <div>EvalBtn</div> }));
vi.mock("@/components/BossHud", () => ({ BossHud: () => <div>BossHud</div> }));
vi.mock("@/components/LayoutSwitcher", () => ({ LayoutSwitcher: () => <div>LayoutSwitcher</div> }));
vi.mock("@/features/workshop/WorkshopGuide", () => ({ WorkshopGuide: () => <div>WorkshopGuide</div> }));
vi.mock("@/components/QuestBoard", () => ({ QuestBoard: () => <div>QuestBoard</div> }));
vi.mock("@/components/EventFeed", () => ({ EventFeed: () => <div>EventFeed</div> }));

describe("DevUI Tutorial Behavior", () => {
    beforeEach(() => {
        window.localStorage.clear();
        vi.clearAllMocks();
    });

    it("auto-opens the Getting Started dialog on first visit", async () => {
        render(
            <MemoryRouter>
                <DevUI />
            </MemoryRouter>
        );

        // Dialog should eventually be visible
        await waitFor(() => {
            expect(screen.getByText(/Welcome to EvalForge/i)).toBeInTheDocument();
        });
    });

    it("clicking 'Start your first quest' navigates to the starter quest and sets storage key", async () => {
        const user = userEvent.setup();
        const navigate = mockNavigateSpy;

        render(
            <MemoryRouter>
                <DevUI />
            </MemoryRouter>
        );

        await screen.findByText(/Welcome to EvalForge/i);

        const startButton = screen.getByRole("button", {
            name: /Start your first quest/i,
        });

        await user.click(startButton);

        expect(window.localStorage.getItem(TUTORIAL_STORAGE_KEY)).toBe("1");
        expect(navigate).toHaveBeenCalledWith(STARTER_QUEST_ROUTE);
    });

    it("respects storage key (does not auto-open) but nav button can re-open the dialog", async () => {
        const user = userEvent.setup();
        window.localStorage.setItem(TUTORIAL_STORAGE_KEY, "1");

        render(
            <MemoryRouter>
                <DevUI />
            </MemoryRouter>
        );

        await waitFor(() => {
            expect(screen.queryByText(/Welcome to EvalForge/i)).not.toBeInTheDocument();
        });

        // Find custom help button
        const navButton = await screen.findByTestId("nav-getting-started");
        await user.click(navButton);

        await screen.findByText(/Welcome to EvalForge/i);
    });
});
