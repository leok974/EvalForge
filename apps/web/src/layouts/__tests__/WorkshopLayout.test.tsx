// Sprint 22: CyberdeckLayout and OrionLayout deleted. Tests updated for unified Workshop.
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

vi.mock('../../components/practice/PracticeGauntletCard', () => ({
    PracticeGauntletCard: () => <div data-testid="mock-gauntlet">Gauntlet</div>
}));

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
        // Default: grid view
        mockUseSettingsStore.mockImplementation((selector: any) => {
            const state = { worldViewMode: 'grid', setWorldViewMode: vi.fn() };
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

    it("List View: renders Gauntlet and sidebar", () => {
        renderLayout('/workshop');
        expect(screen.getByTestId("workshop-tools-panel")).toBeTruthy();
        expect(screen.getByTestId("mock-gauntlet")).toBeTruthy();
        expect(screen.queryByTestId("mock-tools-panel")).toBeNull();
    });

    it("Workbench: hides Gauntlet sidebar, shows workbench content", () => {
        // In workbench mode, showDockedRail = !isWorkbench = false.
        // The aside is not rendered; tools are embedded in the QuestIDE (via Outlet).
        renderLayout('/workshop/quests/test-quest');
        expect(screen.getByTestId("workshop-workbench")).toBeTruthy();
        expect(screen.queryByTestId("workshop-tools-panel")).toBeNull(); // aside hidden in workbench mode
        expect(screen.queryByTestId("mock-gauntlet")).toBeNull(); // gauntlet only in list mode
    });

    it("is always font-sans (Workshop is the only layout)", () => {
        renderLayout('/workshop');
        const main = screen.getByTestId("layout-workshop");
        expect(main.className).toContain("font-sans");
        expect(main.className).not.toContain("font-mono");
    });

    it("shows Board/Map toggle in list view header", () => {
        renderLayout('/workshop');
        expect(screen.getByTitle("Quest Board")).toBeTruthy();
        expect(screen.getByTitle("Star Map")).toBeTruthy();
    });
});
