import React from "react";
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi, describe, it, expect, beforeEach } from "vitest";

import { renderWithRouter } from "../../test/testUtils";
import { PracticeGauntletCard } from "./PracticeGauntletCard";

const mockNavigate = vi.fn();

// Mock react-router-dom navigate but keep everything else
vi.mock("react-router-dom", async (orig) => {
    const actual = await orig();
    return {
        ...actual,
        useNavigate: () => mockNavigate,
    };
});

const multiWorldPayload = {
    date: "2025-12-04",
    label: "Practice Gauntlet – Daily Trials Across Worlds",
    total_count: 3,
    items: [
        {
            id: "quest_review:python-loop",
            item_type: "quest_review",
            label: "Loop Forge",
            difficulty: "medium",
            world_slug: "world-python",
            project_slug: null,
            rationale: "Python Quest",
            struggle_score: 50,
        },
        {
            id: "quest_review:sql-archives",
            item_type: "quest_review",
            label: "Aggregate Archives",
            difficulty: "medium",
            world_slug: "world-sql",
            project_slug: null,
            rationale: "SQL Quest",
            struggle_score: 50,
        },
        {
            id: "boss_review:ml-gradient",
            item_type: "boss_review",
            label: "Gradient Sentinel",
            difficulty: "hard",
            world_slug: "world-ml",
            project_slug: null,
            rationale: "ML Boss",
            struggle_score: 90,
        },
        {
            id: "boss_review:python-foundry-arch",
            item_type: "boss_review",
            label: "Foundry Architect",
            difficulty: "legendary",
            world_slug: "world-python",
            project_slug: null,
            rationale: "Senior Boss",
            struggle_score: 50,
        }
    ],
    completed_count: 0,
    today_quests_completed: 0,
    today_bosses_cleared: 0,
    today_trials_completed: 0,
    streak_days: 3,
    best_streak_days: 7,
};

describe("PracticeGauntletCard – multi-world", () => {
    beforeEach(() => {
        mockNavigate.mockReset();

        // @ts-expect-error - override global fetch
        global.fetch = vi.fn().mockResolvedValue({
            ok: true,
            json: async () => multiWorldPayload,
        });
    });

    it("renders world labels for multiple worlds", async () => {
        const user = userEvent.setup();
        renderWithRouter(<PracticeGauntletCard />);

        // Wait for data load
        // Wait for data load
        await waitFor(() => expect(screen.getByText("Loop Forge")).toBeInTheDocument());

        // Find the buttons (the whole row is a button in current implementation)
        // or specific start buttons. In my updated code, the whole row is likely clickable/button.
        // Let's verify role. The updated code uses <button ... className="group w-full ...">

        const itemButtons = screen.getAllByRole("button");
        // Filter out any other buttons if necessary, but here we expect 3 item buttons
        // Note: Check if there are other buttons rendered by PracticeGauntletCard? 
        // Just the items.

        // Python quest first
        await user.click(itemButtons[0]);
        // Expect routing: /worlds/world-python/quests/python-loop
        // Note: item.id is "quest_review:python-loop", identifier is "python-loop"
        expect(mockNavigate).toHaveBeenCalledWith(
            "/worlds/world-python/quests/python-loop"
        );

        mockNavigate.mockClear();

        // SQL quest second
        await user.click(itemButtons[1]);
        // Expect routing: /worlds/world-sql/quests/sql-archives
        expect(mockNavigate).toHaveBeenCalledWith(
            "/worlds/world-sql/quests/sql-archives"
        );

        mockNavigate.mockClear();

        // ML boss third
        await user.click(itemButtons[2]);
        // Expect routing: /worlds/world-ml/bosses/ml-gradient
        expect(mockNavigate).toHaveBeenCalledWith(
            "/worlds/world-ml/bosses/ml-gradient"
        );

        // Legendary check
        const legendaryBadge = screen.getByText("Legendary Boss");
        expect(legendaryBadge).toBeInTheDocument();
        expect(legendaryBadge).toHaveClass("animate-pulse");
    });
});
