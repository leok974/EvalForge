import React from "react";
import { render, screen } from "@testing-library/react";
import { WorkshopLayout } from "../WorkshopLayout";
import { describe, it, expect } from "vitest";
import { MemoryRouter } from 'react-router-dom';

describe("WorkshopLayout – damage flashes", () => {
    it("adds a hit ring when integrityDelta < 0", () => {
        render(
            <MemoryRouter>
                <WorkshopLayout
                    bossHud={<div />}
                    worldSelector={<div />}
                    questPanel={<div />}
                    projectPanel={<div />}
                    codexPanel={<div />}
                    activityFeed={<div />}
                    integrityDelta={-10}
                    bossHpDelta={0}
                />
            </MemoryRouter>
        );

        const bench = screen.getByTestId("workshop-workbench");
        const className = bench.className;
        expect(className).toMatch(/ring-rose-500\/80/);
    });

    it("adds a hit ring when bossHpDelta < 0", () => {
        render(
            <MemoryRouter>
                <WorkshopLayout
                    bossHud={<div />}
                    worldSelector={<div />}
                    questPanel={<div />}
                    projectPanel={<div />}
                    codexPanel={<div />}
                    activityFeed={<div />}
                    integrityDelta={0}
                    bossHpDelta={-40}
                />
            </MemoryRouter>
        );

        const bench = screen.getByTestId("workshop-workbench");
        const className = bench.className;
        expect(className).toMatch(/ring-emerald-400\/80/);
    });
});
