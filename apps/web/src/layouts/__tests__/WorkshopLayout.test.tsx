import React from "react";
import { render, screen } from "@testing-library/react";
import { WorkshopLayout } from "../WorkshopLayout";
import { describe, it, expect } from "vitest";

describe("WorkshopLayout", () => {
    it("renders core slots and data-testids", () => {
        render(
            <WorkshopLayout
                bossHud={<div>BossHudSlot</div>}
                worldSelector={<div>WorldSelectorSlot</div>}
                questPanel={<div>QuestPanelSlot</div>}
                projectPanel={<div>ProjectPanelSlot</div>}
                codexPanel={<div>CodexPanelSlot</div>}
                activityFeed={<div>ActivityFeedSlot</div>}
            />
        );

        expect(screen.getByTestId("layout-workshop")).toBeTruthy();
        expect(screen.getByTestId("workshop-workbench")).toBeTruthy();
        expect(screen.getByTestId("workshop-project-bench")).toBeTruthy();
        expect(screen.getByTestId("workshop-codex-shelf")).toBeTruthy();
        expect(screen.getByTestId("workshop-activity-strip")).toBeTruthy();

        expect(screen.getByText("BossHudSlot")).toBeTruthy();
        expect(screen.getByText("QuestPanelSlot")).toBeTruthy();
        expect(screen.getByText("ProjectPanelSlot")).toBeTruthy();
    });
});
