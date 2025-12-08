import { render, screen, fireEvent } from "@testing-library/react";
import { PracticeGauntletCard } from "../practice/PracticeGauntletCard";
import { BrowserRouter } from "react-router-dom";

// Mock fetch
global.fetch = jest.fn();

// Mock navigate
const mockedNavigate = jest.fn();
jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useNavigate: () => mockedNavigate
}));

describe("PracticeGauntlet Legendary Visuals", () => {
    const mockPlan = {
        date: "2025-12-08",
        label: "Today",
        items: [
            {
                id: "boss:legendary-boss",
                item_type: "boss_review",
                label: "Legendary Boss",
                description: "",
                difficulty: "legendary",
                rationale: "Testing",
                struggle_score: 5,
                world_slug: "world-test"
            },
            {
                id: "boss:normal-boss",
                item_type: "boss_review",
                label: "Normal Boss",
                description: "",
                difficulty: "hard",
                rationale: "Testing",
                struggle_score: 3,
                world_slug: "world-test"
            }
        ],
        completed_count: 0,
        total_count: 2,
        streak_days: 5
    };

    beforeEach(() => {
        (global.fetch as jest.Mock).mockReset();
        mockedNavigate.mockReset();
    });

    it("styles legendary items distinctively", async () => {
        (global.fetch as jest.Mock).mockResolvedValueOnce({
            ok: true,
            json: async () => mockPlan
        });

        render(
            <BrowserRouter>
                <PracticeGauntletCard />
            </BrowserRouter>
        );

        const legendaryCard = await screen.findByTestId("gauntlet-card-legendary-boss:legendary-boss");
        const normalCard = await screen.findByTestId("gauntlet-card-normal-boss:normal-boss");

        expect(legendaryCard).toBeInTheDocument();
        expect(normalCard).toBeInTheDocument();

        // Check legendary styling
        expect(legendaryCard.className).toContain("border-amber-400");

        // Click navigation check
        fireEvent.click(legendaryCard);
        expect(mockedNavigate).toHaveBeenCalledWith("/worlds/world-test/bosses/legendary-boss");
    });
});
