
import React from "react";
import { render, screen } from "@testing-library/react";
import { QuestResultPanel } from "../QuestResultPanel";
import type { QuestSubmitResult } from "@/lib/questsApi";

describe("QuestResultPanel", () => {
    it("renders XP and unlock chips when present", () => {
        const result: QuestSubmitResult = {
            quest: {
                id: 1,
                slug: "python-reactor-prep",
                world_id: "world-python",
                track_id: "boss-prep",
                order_index: 3,
                title: "Reactor Prep",
                short_description: "Prepare for the Reactor Core boss.",
                state: "completed",
                best_score: 97.5,
                attempts: 1,
                unlocks_boss_id: "reactor-core",
                unlocks_layout_id: "orion",
                base_xp_reward: 50,
                mastery_xp_bonus: 25,
            },
            score: 97.5,
            passed: true,
            xp_awarded: 75,
            unlock_events: [
                { type: "boss", id: "reactor-core", label: "Reactor Core" },
                { type: "layout", id: "orion", label: "Orion Deck" },
            ],
        };

        render(<QuestResultPanel result={result} />);

        // Panel shows up
        expect(screen.getByTestId("quest-result-panel")).toBeTruthy();

        // XP chip
        const xpChip = screen.getByTestId("quest-result-xp");
        expect(xpChip.textContent).toContain("+75 XP");

        // Boss unlock chip
        const bossChip = screen.getByTestId("quest-unlock-boss-reactor-core");
        expect(bossChip.textContent).toMatch(/Boss unlocked: Reactor Core/i);

        // Layout unlock chip
        const layoutChip = screen.getByTestId("quest-unlock-layout-orion");
        expect(layoutChip.textContent).toMatch(/Layout unlocked: Orion Deck/i);
    });

    it("renders nothing when result is null", () => {
        const { container } = render(<QuestResultPanel result={null} />);
        expect(container.firstChild).toBeNull();
    });
});
