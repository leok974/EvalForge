
// @vitest-environment jsdom
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { WorkshopToolsPanel } from '../WorkshopToolsPanel';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import * as ToolsApi from '../../../lib/toolsApi';
import { useQuestStore } from '../../../store/questStore';

// Mock dependencies
vi.mock('../../../lib/toolsApi', () => ({
    explainQuest: vi.fn(),
    debugQuest: vi.fn()
}));

vi.mock('../../../store/questStore', () => ({
    useQuestStore: vi.fn()
}));

vi.mock('../../../features/codex/CodexPanel', () => ({
    CodexPanel: () => <div>Codex Mock</div>
}));

vi.mock('../../../features/workshop/workshopPanels', () => ({
    PanelId: {},
    WORKSHOP_PANELS: {
        judge: { id: 'judge', label: 'Judge', description: 'Run code', isEnabled: () => true },
        explain: { id: 'explain', label: 'Explain', description: 'Get help', isEnabled: () => true },
        debug: { id: 'debug', label: 'Debug', description: 'Fix bugs', isEnabled: () => true },
        codex: { id: 'codex', label: 'Codex', description: 'Reference', isEnabled: () => true }
    }
}));

describe('WorkshopToolsPanel', () => {
    const mockOnPanelChange = vi.fn();
    const mockHasSkill = vi.fn().mockReturnValue(true);

    beforeEach(() => {
        vi.clearAllMocks();
        (useQuestStore as any).mockReturnValue({
            lastRunResult: null
        });
    });

    it('renders tabs correctly', () => {
        render(
            <WorkshopToolsPanel
                activePanel="judge"
                onPanelChange={mockOnPanelChange}
                hasSkill={mockHasSkill}
                questSlug="test-quest"
            />
        );
        expect(screen.getByText('Judge')).toBeTruthy();
        expect(screen.getByText('Explain')).toBeTruthy();
        expect(screen.getByText('Debug')).toBeTruthy();
    });

    it('Explain tab shows empty state initially', () => {
        render(
            <WorkshopToolsPanel
                activePanel="explain"
                onPanelChange={mockOnPanelChange}
                hasSkill={mockHasSkill}
                questSlug="test-quest"
            />
        );
        expect(screen.getByText('Run Code First')).toBeTruthy();
    });

    it('Explain tab enables button when lastRunResult is present', () => {
        (useQuestStore as any).mockReturnValue({
            lastRunResult: { stdout: "foo", stderr: null }
        });

        render(
            <WorkshopToolsPanel
                activePanel="explain"
                onPanelChange={mockOnPanelChange}
                hasSkill={mockHasSkill}
                questSlug="test-quest"
            />
        );

        const btn = screen.getByText('Analyze Last Run');
        expect(btn).toBeTruthy();
        expect(btn).not.toBeDisabled();
    });

    it('Clicking Analyze calls API', async () => {
        (useQuestStore as any).mockReturnValue({
            lastRunResult: { stdout: "foo", stderr: null, test_summary: { failures: [] } }
        });
        (ToolsApi.explainQuest as any).mockResolvedValue({
            summary: "Test Summary",
            what_happened: "It worked",
            why_it_failed: "It didn't",
            next_steps: [],
            relevant_codex_refs: []
        });

        render(
            <WorkshopToolsPanel
                activePanel="explain"
                onPanelChange={mockOnPanelChange}
                hasSkill={mockHasSkill}
                questSlug="test-quest"
            />
        );

        fireEvent.click(screen.getByText('Analyze Last Run'));

        expect(screen.getByText('Running Analysis...')).toBeTruthy();

        await waitFor(() => {
            expect(ToolsApi.explainQuest).toHaveBeenCalledWith(expect.objectContaining({
                quest_slug: "test-quest",
                stdout: "foo"
            }));
        });

        expect(screen.getByText('Test Summary')).toBeTruthy();
    });

    it('Debug tab calls API and renders results', async () => {
        (useQuestStore as any).mockReturnValue({
            lastRunResult: { stdout: "", stderr: "Error", test_summary: { failures: [] } }
        });
        (ToolsApi.debugQuest as any).mockResolvedValue({
            summary: "Crash Detected",
            likely_root_causes: ["Bad code"],
            fix_plan: ["Fix it"],
            patch_proposal: null
        });

        render(
            <WorkshopToolsPanel
                activePanel="debug"
                onPanelChange={mockOnPanelChange}
                hasSkill={mockHasSkill}
                questSlug="test-quest"
            />
        );

        fireEvent.click(screen.getByText('Debug Last Failure'));
        await waitFor(() => {
            expect(screen.getByText('Crash Detected')).toBeTruthy();
            expect(screen.getByText('Bad code')).toBeTruthy();
        });
    });
});
