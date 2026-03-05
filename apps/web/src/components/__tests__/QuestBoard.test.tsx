import React from "react";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { QuestBoard } from "../QuestBoard";
import { vi, describe, beforeEach, it, expect } from "vitest";
import { BrowserRouter } from "react-router-dom";

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

const mockResolveCanonicalTrackId = vi.fn().mockImplementation((id) => id);
const mockGetTracksForWorld = vi.fn().mockReturnValue([
    { track_id: "fundamentals", name: "Fundamentals" },
]);
const mockResolveTrackName = vi.fn().mockImplementation((t) => t.name || t.track_id);
const mockResolveWorldName = vi.fn().mockReturnValue("Python World");

vi.mock("@/features/workshop/WorkshopCatalogContext", () => ({
    useWorkshopCatalog: () => ({
        getTracksForWorld: mockGetTracksForWorld,
        resolveTrackName: mockResolveTrackName,
        resolveWorldName: mockResolveWorldName,
        resolveCanonicalTrackId: mockResolveCanonicalTrackId,
        worlds: [{ world_id: "world-python", name: "Python World" }],
        tracks: [{ track_id: "fundamentals", name: "Fundamentals" }],
    }),
}));

vi.mock("@/config/devFlags", () => ({
    isGodModeEnabledFromEnv: vi.fn().mockReturnValue(false),
}));

describe("QuestBoard", () => {
    beforeEach(() => {
        vi.clearAllMocks();
        mockFetchQuests.mockResolvedValue([
            {
                id: 1,
                slug: "python-ignition",
                world_id: "world-python",
                track_id: "fundamentals", // Note: will be normalized to track-python-fundamentals if catalog works
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
            {
                id: 2,
                slug: "locked-quest",
                world_id: "world-python",
                track_id: "fundamentals",
                order_index: 2,
                title: "Locked",
                short_description: "Locked test quest.",
                state: "locked",
                best_score: null,
                attempts: 0,
                base_xp_reward: 50,
                mastery_xp_bonus: 25,
            }
        ]);
    });

    it("renders quests and allows accepting", async () => {
        const onOpenQuest = vi.fn();

        render(
            <BrowserRouter>
                <QuestBoard worldId="world-python" onOpenQuest={onOpenQuest} />
            </BrowserRouter>
        );

        const board = await screen.findByTestId("quest-board");
        expect(board).toBeInTheDocument();

        const actionBtn = screen.getByTestId("quest-action-python-ignition");
        expect(actionBtn).toHaveTextContent(/accept/i);

        fireEvent.click(actionBtn);

        await waitFor(() => {
            expect(onOpenQuest).toHaveBeenCalledTimes(1);
        });

        // Locked quest should say Locked
        const lockedBtn = screen.getByTestId("quest-action-locked-quest");
        expect(lockedBtn).toHaveTextContent(/locked/i);
        expect(lockedBtn).toBeDisabled();
    });

    it("unlocks locked quests if God Mode is enabled", async () => {
        // Force the mock to return true for this test
        const devFlags = await import("@/config/devFlags");
        vi.mocked(devFlags.isGodModeEnabledFromEnv).mockReturnValue(true);

        render(
            <BrowserRouter>
                <QuestBoard worldId="world-python" />
            </BrowserRouter>
        );

        const board = await screen.findByTestId("quest-board");
        expect(board).toBeInTheDocument();

        // Locked quest should now say Accept
        const unlockedBtn = screen.getByTestId("quest-action-locked-quest");
        expect(unlockedBtn).toHaveTextContent(/accept/i);
        expect(unlockedBtn).not.toBeDisabled();
    });
});
