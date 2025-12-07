import React from "react";
import { render, screen } from "@testing-library/react";
import { WorkshopLayout } from "../WorkshopLayout";
import { describe, it, expect } from "vitest";
import { MemoryRouter } from 'react-router-dom';

describe("WorkshopLayout – activity ripple", () => {
    beforeEach(() => {
        vi.useFakeTimers();
    });

    afterEach(() => {
        vi.useRealTimers();
    });

    it("adds a ripple class to the activity strip when a hit occurs and removes it after timeout", async () => {
        const { rerender } = render(
            <MemoryRouter>
                <WorkshopLayout
                    bossHud={<div />}
                    worldSelector={<div />}
                    questPanel={<div />}
                    projectPanel={<div />}
                    codexPanel={<div />}
                    activityFeed={<div />}
                    integrityDelta={0}
                    bossHpDelta={0}
                />
            </MemoryRouter>
        );

        // Initial state: No ripple
        const strip = screen.getByTestId("workshop-activity-strip");
        expect(strip.className).not.toMatch(/ring-emerald-300\/70/);

        // Trigger Hit (Boss took damage -> activity ripple)
        rerender(
            <MemoryRouter>
                <WorkshopLayout
                    bossHud={<div />}
                    worldSelector={<div />}
                    questPanel={<div />}
                    projectPanel={<div />}
                    codexPanel={<div />}
                    activityFeed={<div />}
                    integrityDelta={0}
                    bossHpDelta={-20} // Hit!
                />
            </MemoryRouter>
        );

        // Check ripple is present
        expect(strip.className).toMatch(/ring-emerald-300\/70/);

        // Fast-forward time (timeout is 260ms)
        await React.act(async () => {
            vi.advanceTimersByTime(300);
        });

        // Check ripple is removed
        expect(strip.className).not.toMatch(/ring-emerald-300\/70/);
    });
});
