import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LadderPanel } from "../LadderPanel";
import { useGameStore } from "@/store/gameStore";
import { expect, vi, describe, it, beforeEach } from "vitest";
import { MemoryRouter } from "react-router-dom";

// Mock fetch
global.fetch = vi.fn();

// Mock useNavigate
const mockNavigate = vi.fn();
vi.mock("react-router-dom", async () => {
    const actual = await vi.importActual("react-router-dom");
    return {
        ...actual,
        useNavigate: () => mockNavigate,
    };
});

describe("LadderPanel highlight auto-clear", () => {
    const mockLadder = {
        ladder_id: "test-ladder",
        slug: "test-ladder",
        title: "Test Ladder",
        summary: "A test ladder",
        stages: [
            {
                stage_id: "stage-1",
                order_index: 1,
                title: "Stage 1",
                description: "Desc",
                nodes: [
                    { id: "q1", kind: "quest", label: "First", order_index: 1 },
                    { id: "q2", kind: "quest", label: "Second", order_index: 2 }
                ]
            }
        ],
        completion_rewards: { titles: ["Master"] }
    };

    beforeEach(() => {
        vi.resetAllMocks();
        (global.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => mockLadder
        });

        // Reset store
        useGameStore.setState({
            highlightedQuestId: null,
            activeTrack: null // clear other state if needed
        });
    });

    it("clears the highlight when the highlighted quest node is clicked", async () => {
        const user = userEvent.setup();

        // Pretend q2 is highlighted
        useGameStore.setState({ highlightedQuestId: "q2" });

        render(
            <MemoryRouter>
                <LadderPanel worldSlug="world-test" />
            </MemoryRouter>
        );

        // Wait for nodes to load
        await waitFor(() => {
            expect(screen.getByText("Second")).toBeInTheDocument();
        });

        const secondNode = screen.getByText("Second").closest("[data-testid^='ladder-node-']")!;

        // Assert styling or data attribute
        expect(secondNode).toHaveAttribute("data-highlighted", "true");

        // Click it
        await user.click(secondNode);

        // Check Highlight Cleared in Store
        const state = useGameStore.getState();
        expect(state.highlightedQuestId).toBeNull();

        // Check Navigation
        expect(mockNavigate).toHaveBeenCalledWith("/quests/q2");

        // Check UI update (optional, but good)
        // Note: Re-rendering might take a tick, but the attribute should update
        // expect(secondNode).toHaveAttribute("data-highlighted", "false"); 
    });
});
