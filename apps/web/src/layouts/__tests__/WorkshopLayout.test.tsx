// @vitest-environment jsdom
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { WorkshopLayout } from "../WorkshopLayout";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import * as LayoutHooks from '../../hooks/useCurrentLayout';

// Bypass alias issues (using relative path to ensured matching)
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

vi.mock('../../store/questStore', () => ({
    useQuestStore: (selector: any) => mockUseQuestStore(selector)
}));

vi.mock('../../store/gameStore', () => ({
    useGameStore: (selector: any) => mockUseGameStore(selector)
}));

describe("WorkshopLayout", () => {
    beforeEach(() => {
        vi.clearAllMocks();
        // Default Store Mocks
        mockUseQuestStore.mockImplementation((selector: any) => {
            // Mock state
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
    });

    const renderLayout = (layoutId: 'orion' | 'cyberdeck', path = '/workshop') => {
        // Mock Layout Context
        vi.spyOn(LayoutHooks, 'useCurrentLayout').mockReturnValue({
            layout: layoutId,
            setLayout: vi.fn()
        });

        return render(
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
    };

    it("List View: Renders Gauntlet and always shows Sidebar", () => {
        // Path does not have questId -> List View
        renderLayout('orion', '/workshop');

        // Sidebar should be present in List View even for Orion
        expect(screen.getByTestId("workshop-tools-panel")).toBeTruthy();
        expect(screen.getByTestId("mock-gauntlet")).toBeTruthy();
        // Tools Panel component is NOT rendered in List View (we render direct content)
        expect(screen.queryByTestId("mock-tools-panel")).toBeNull();
    });

    it("Workbench (Cyberdeck): Renders Tools Panel Docked", () => {
        // Path has questId -> Workbench
        // Cyberdeck -> Sidebar Visible
        renderLayout('cyberdeck', '/workshop/quests/test-quest');

        expect(screen.getByTestId("workshop-tools-panel")).toBeTruthy();
        expect(screen.getByTestId("mock-tools-panel")).toBeTruthy();
        // Gauntlet hidden in workbench
        expect(screen.queryByTestId("mock-gauntlet")).toBeNull();
    });

    it("Workbench (Orion): Sidebar Collapsed/Hidden initially", () => {
        // Path has questId -> Workbench
        // Orion -> Sidebar Hidden
        renderLayout('orion', '/workshop/quests/test-quest');

        expect(screen.queryByTestId("workshop-tools-panel")).toBeNull();

        // Should verify Tools button exists
        expect(screen.getByText("Tools", { selector: 'button' })).toBeTruthy();
    });

    it("Workbench (Orion): Can toggle Tools Overlay", async () => {
        renderLayout('orion', '/workshop/quests/test-quest');

        const toggle = screen.getByText("Tools", { selector: 'button' });
        fireEvent.click(toggle);

        // Expect Overlay to appear containing ToolsPanel
        expect(screen.getByTestId("mock-tools-panel")).toBeTruthy();
    });
    it("List View: Applies layout-specific visual styles", () => {
        // Orion -> font-sans
        const { unmount } = renderLayout('orion', '/workshop');
        const mainOrion = screen.getByTestId("layout-workshop");
        expect(mainOrion.className).toContain("font-sans");
        expect(mainOrion.className).not.toContain("font-mono");
        unmount();

        // Cyberdeck -> font-mono
        renderLayout('cyberdeck', '/workshop');
        const mainCyber = screen.getByTestId("layout-workshop");
        expect(mainCyber.className).toContain("font-mono");
        expect(mainCyber.className).not.toContain("font-sans");
    });
});

