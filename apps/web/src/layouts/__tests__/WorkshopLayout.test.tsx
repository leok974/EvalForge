// Sprint 22: CyberdeckLayout and OrionLayout deleted. Tests updated for unified Workshop.
// Sprint 22.6: worldViewMode/Map toggle rolled back — Board is the only view.
// Sprint 23: Intent Oracle and Practice Gauntlet stub panels removed.
//            Right rail (aside) deleted — quest list is now full-width in all views.
// @vitest-environment jsdom
import React from "react";
import { render, screen } from "@testing-library/react";
import { WorkshopLayout } from "../WorkshopLayout";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter, Route, Routes } from 'react-router-dom';

vi.mock('../../lib/worldProgressEvents', () => ({
    subscribeWorldProgress: vi.fn(),
    emitWorldProgress: vi.fn()
}));

vi.mock('../../features/workshop/useWorkshopTips', () => ({
    openWorkshopGuide: vi.fn()
}));

vi.mock('../../components/workshop/WorkshopToolsPanel', () => ({
    WorkshopToolsPanel: () => <div data-testid="mock-tools-panel">ToolsPanel</div>
}));

// Sprint 23: PracticeGauntletCard deleted — mock no longer needed.

// Mock Stores
const mockUseQuestStore = vi.fn();
const mockUseGameStore = vi.fn();
const mockUseSettingsStore = vi.fn();

vi.mock('../../store/questStore', () => ({
    useQuestStore: (selector: any) => mockUseQuestStore(selector)
}));

vi.mock('../../store/gameStore', () => ({
    useGameStore: (selector: any) => mockUseGameStore(selector)
}));

vi.mock('../../store/settingsStore', () => ({
    useSettingsStore: (selector: any) => mockUseSettingsStore(selector)
}));

describe("WorkshopLayout", () => {
    beforeEach(() => {
        vi.clearAllMocks();
        mockUseQuestStore.mockImplementation((selector: any) => {
            const state = {
                setActiveWorldSlug: vi.fn(),
                setActiveTrackId: vi.fn(),
                setActiveBossSlug: vi.fn(),
                focusMode: false
            };
            return selector(state);
        });
        mockUseGameStore.mockImplementation((selector: any) => {
            const state = { activeTrack: { label: 'Test Project' } };
            return selector(state);
        });
        // Sprint 22.6: worldViewMode removed — Board is the only view.
        mockUseSettingsStore.mockImplementation((selector: any) => {
            const state = { screenShake: true, particles: true };
            return selector ? selector(state) : state;
        });
    });

    const renderLayout = (path = '/workshop') => render(
        <MemoryRouter initialEntries={[path]}>
            <Routes>
                <Route path="/workshop" element={
                    <WorkshopLayout
                        bossHud={<div>BossHud</div>}
                        worldSelector={<div>WorldSelector</div>}
                        questPanel={<div>QuestPanelContent</div>}
                        projectPanel={<div>ProjectPanel</div>}
                        codexPanel={<div>CodexPanel</div>}
                        activityFeed={<div>ActivityFeed</div>}
                    />
                }>
                    <Route path="quests/:questId" element={<div>Quest Mode</div>} />
                </Route>
            </Routes>
        </MemoryRouter>
    );

    it("List View: renders quest board full-width (no stub panels)", () => {
        // Sprint 23: No right-rail aside. Quest list is the primary content.
        renderLayout('/workshop');
        expect(screen.getByTestId("workshop-workbench")).toBeTruthy();
        expect(screen.getByText("QuestPanelContent")).toBeTruthy();
        // Stub panels removed
        expect(screen.queryByText("Intent Oracle")).toBeNull();
        expect(screen.queryByTestId("mock-gauntlet")).toBeNull();
        // WorkshopToolsPanel is not rendered in list view (it's inside QuestIDE)
        expect(screen.queryByTestId("mock-tools-panel")).toBeNull();
    });

    it("Workbench: shows workbench content (quest IDE), no stub panels", () => {
        renderLayout('/workshop/quests/test-quest');
        expect(screen.getByTestId("workshop-workbench")).toBeTruthy();
        expect(screen.queryByText("Intent Oracle")).toBeNull();
        expect(screen.queryByTestId("mock-gauntlet")).toBeNull();
    });

    it("is always font-sans (Workshop is the only layout)", () => {
        renderLayout('/workshop');
        const main = screen.getByTestId("layout-workshop");
        expect(main.className).toContain("font-sans");
        expect(main.className).not.toContain("font-mono");
    });

    it("shows no Map toggle (Board is the only world-selection view)", () => {
        // Sprint 22.6: Map toggle removed. No 'Star Map' or 'Quest Board' title buttons.
        renderLayout('/workshop');
        expect(screen.queryByTitle("Quest Board")).toBeNull();
        expect(screen.queryByTitle("Star Map")).toBeNull();
    });
});
