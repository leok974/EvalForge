import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, beforeEach, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { PracticeGauntletCard } from "./PracticeGauntletCard";

describe("PracticeGauntletCard", () => {
    beforeEach(() => {
        vi.resetAllMocks();
    });

    it("renders header and hits the API", async () => {
        const mockPlan = {
            date: "2025-12-04",
            label: "Practice Gauntlet",
            completed_count: 0,
            total_count: 1,
            streak_days: 3,
            items: [
                {
                    id: "boss_review:reactor-core",
                    item_type: "boss_review",
                    label: "Reactor Core",
                    description: "",
                    world_slug: "world-python",
                    project_slug: null,
                    difficulty: "hard",
                    rationale: "You struggled with this recently—time for a focused rematch.",
                    struggle_score: 85,
                },
            ],
        };

        const fetchMock = vi.fn().mockResolvedValue({
            ok: true,
            json: async () => mockPlan,
        } as any);

        // @ts-expect-error - override global fetch in tests
        global.fetch = fetchMock;


        render(
            <MemoryRouter>
                <PracticeGauntletCard />
            </MemoryRouter>
        );


        expect(
            screen.getByTestId("practice-gauntlet-card")
        ).toBeInTheDocument();
        expect(
            screen.getByText(/Practice Gauntlet/i)
        ).toBeInTheDocument();

        await waitFor(() =>
            expect(
                screen.getByTestId("practice-gauntlet-items")
            ).toBeInTheDocument()
        );

        expect(screen.getByText(/Reactor Core/)).toBeInTheDocument();
        expect(fetchMock).toHaveBeenCalledWith(
            "/api/practice_rounds/today",
            expect.any(Object)
        );
    });

    it("shows error state when API fails", async () => {
        const fetchMock = vi.fn().mockResolvedValue({
            ok: false,
            status: 500,
            text: async () => "Server error",
        } as any);

        // @ts-expect-error - override global fetch in tests
        global.fetch = fetchMock;

        render(
            <MemoryRouter>
                <PracticeGauntletCard />
            </MemoryRouter>
        );

        await waitFor(() =>
            expect(
                screen.getByTestId("practice-gauntlet-error")
            ).toBeInTheDocument()
        );

        expect(screen.getByText(/Practice Gauntlet unavailable/)).toBeInTheDocument();
    });

    it("shows empty state when no items", async () => {
        const mockPlan = {
            date: "2025-12-04",
            label: "Practice Gauntlet",
            completed_count: 0,
            total_count: 0,
            items: [],
        };

        const fetchMock = vi.fn().mockResolvedValue({
            ok: true,
            json: async () => mockPlan,
        } as any);

        // @ts-expect-error - override global fetch in tests
        global.fetch = fetchMock;

        render(
            <MemoryRouter>
                <PracticeGauntletCard />
            </MemoryRouter>
        );

        await waitFor(() =>
            expect(
                screen.getByTestId("practice-gauntlet-empty")
            ).toBeInTheDocument()
        );

        expect(screen.getByText(/No specific targets today/)).toBeInTheDocument();
    });
});
