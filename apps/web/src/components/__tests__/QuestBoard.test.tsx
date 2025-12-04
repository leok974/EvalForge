
import React from "react";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { QuestBoard } from "../QuestBoard";
import { vi } from "vitest";

const mockFetchQuests = vi.fn();

vi.mock("@/lib/questsApi", () => ({
    fetchQuests: (worldId?: string) => mockFetchQuests(worldId),
    acceptQuest: vi.fn().mockResolvedValue({
        id: 1,
        slug: "python-ignition",
        world_id: "world-python",
        track_id: "fundamentals",
        order_index: 1,
        title: "Ignition",
        short_description: "Warm up your Python engine.",
        state: "in_progress",
        best_score: null,
        attempts: 1,
        unlocks_boss_id: "reactor-core",
        unlocks_layout_id: "orion",
        base_xp_reward: 50,
        mastery_xp_bonus: 25,
    }),
}));

describe("QuestBoard", () => {
    beforeEach(() => {
        mockFetchQuests.mockResolvedValue([
            {
                id: 1,
                slug: "python-ignition",
                world_id: "world-python",
                track_id: "fundamentals",
                order_index: 1,
                title: "Ignition",
                short_description: "Warm up your Python engine.",
                state: "available",
                best_score: null,
                attempts: 0,
                unlocks_boss_id: "reactor-core",
                unlocks_layout_id: "orion",
                base_xp_reward: 50,
                mastery_xp_bonus: 25,
            },
        ]);
    });

    it("renders quests and allows accepting", async () => {
        const onOpenQuest = vi.fn();

        render(<QuestBoard worldId="world-python" onOpenQuest={onOpenQuest} />);

        await waitFor(() =>
            expect(screen.getByTestId("quest-board")).toBeTruthy()
        );

        const actionBtn = screen.getByTestId("quest-action-python-ignition");
        expect(actionBtn.textContent).toMatch(/accept/i);

        fireEvent.click(actionBtn);

        await waitFor(() => {
            expect(onOpenQuest).toHaveBeenCalledTimes(1);
        });
    });
});
