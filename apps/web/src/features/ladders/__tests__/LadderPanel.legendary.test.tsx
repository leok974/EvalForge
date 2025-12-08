import { render, screen, waitFor } from "@testing-library/react";
import { LadderPanel } from "../LadderPanel";
import { LadderSpec } from "../types";

// Mock fetch
global.fetch = jest.fn();

describe("LadderPanel Legendary Visuals", () => {
    const mockLadder: LadderSpec = {
        ladder_id: "test-ladder",
        slug: "test-ladder",
        title: "Test Ladder",
        summary: "A test ladder",
        recommended_entry_level: "beginner",
        recommended_exit_level: "intermediate",
        tags: [],
        stages: [
            {
                stage_id: "stage-1",
                order_index: 1,
                title: "Stage 1",
                description: "Desc",
                goals: [],
                quests: [],
                bosses: [],
                nodes: [
                    { id: "boss-legacy", kind: "boss", label: "Normal Boss", order_index: 1 },
                    { id: "boss-legendary", kind: "legendary_boss", label: "Legendary Boss", order_index: 2 }
                ]
            }
        ],
        completion_rewards: { xp: 100, titles: ["Master"], unlocks: [] }
    };

    beforeEach(() => {
        (global.fetch as jest.Mock).mockReset();
    });

    it("renders legendary nodes with distinct styling", async () => {
        (global.fetch as jest.Mock).mockResolvedValueOnce({
            ok: true,
            json: async () => mockLadder
        });

        render(<LadderPanel worldSlug="world-test" />);

        await waitFor(() => {
            expect(screen.getByText("Legendary Boss")).toBeInTheDocument();
        });

        const legendaryNode = screen.getByTestId("ladder-node-legendary-boss-legendary");
        const normalNode = screen.getByTestId("ladder-node-normal-boss-legacy");

        expect(legendaryNode).toBeInTheDocument();
        expect(normalNode).toBeInTheDocument();

        // Check for amber styling class presence (partial match)
        expect(legendaryNode.className).toContain("amber-400");
        expect(legendaryNode.className).toContain("shadow");

        // Normal node should not have amber
        expect(normalNode.className).not.toContain("amber-400");
    });
});
