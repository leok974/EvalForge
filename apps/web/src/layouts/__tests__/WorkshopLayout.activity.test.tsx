import React from "react";
import { render, screen } from "@testing-library/react";
import { WorkshopLayout } from "../WorkshopLayout";
import { describe, it, expect } from "vitest";

describe("WorkshopLayout – activity ripple", () => {
    it("adds a ripple class to the activity strip when a hit occurs", () => {
        render(
            <WorkshopLayout
                bossHud={<div />}
                worldSelector={<div />}
                questPanel={<div />}
                projectPanel={<div />}
                codexPanel={<div />}
                activityFeed={<div />}
                integrityDelta={0}
                bossHpDelta={-20}
            />
        );

        const strip = screen.getByTestId("workshop-activity-strip");
        expect(strip.className).toMatch(/ring-emerald-300\/70/);
    });
});
