import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import DevQA from '../DevQA';

// Mock the qaApi module
vi.mock('../../lib/qaApi', () => ({
    getQASummary: vi.fn(),
    getQAQuests: vi.fn(),
    runQATest: vi.fn(),
    pollQARun: vi.fn(),
}));

import { getQASummary, getQAQuests, runQATest, pollQARun } from '../../lib/qaApi';

const mockSummary = {
    generated_at: '2026-01-31T12:00:00Z',
    tracks: [
        {
            world_id: 'foundry',
            track_id: 'beginner',
            quests_total: 10,
            healthy: 8,
            unhealthy: 2,
            unknown: 0,
        },
    ],
    global: {
        quests_total: 100,
        healthy: 85,
        unhealthy: 10,
        unknown: 5,
    },
};

const mockQuests = {
    quests: [
        {
            slug: 'quest-test-1',
            title: 'Test Quest 1',
            world_id: 'foundry',
            track_id: 'beginner',
            language: 'python',
            health_status: 'healthy',
            last_run_at: '2026-01-31T11:00:00Z',
            last_run_variant: 'integrity',
        },
        {
            slug: 'quest-test-2',
            title: 'Test Quest 2',
            world_id: 'prism',
            track_id: 'advanced',
            language: 'typescript',
            health_status: 'unhealthy',
            last_run_at: null,
            last_run_variant: null,
        },
    ],
};

describe('DevQA Dashboard', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        (getQASummary as any).mockResolvedValue(mockSummary);
        (getQAQuests as any).mockResolvedValue(mockQuests);
    });

    it('renders overview cards with correct metrics', async () => {
        render(
            <BrowserRouter>
                <DevQA />
            </BrowserRouter>
        );

        // Wait for data to load
        await waitFor(() => {
            expect(screen.getByText('100')).toBeInTheDocument(); // Total quests
        });

        expect(screen.getByText('85')).toBeInTheDocument(); // Healthy
        expect(screen.getByText('10')).toBeInTheDocument(); // Unhealthy
        expect(screen.getByText('5')).toBeInTheDocument(); // Unknown
    });

    it('renders quest grid with quest data', async () => {
        render(
            <BrowserRouter>
                <DevQA />
            </BrowserRouter>
        );

        await waitFor(() => {
            expect(screen.getByText('Test Quest 1')).toBeInTheDocument();
        });

        expect(screen.getByText('Test Quest 2')).toBeInTheDocument();
        expect(screen.getByText('quest-test-1')).toBeInTheDocument();
        expect(screen.getByText('quest-test-2')).toBeInTheDocument();
    });

    it('filters quests by world', async () => {
        const mockFilteredQuests = {
            quests: [mockQuests.quests[0]], // Only foundry quest
        };

        (getQAQuests as any)
            .mockResolvedValueOnce(mockQuests) // Initial load
            .mockResolvedValueOnce(mockFilteredQuests); // After filter

        render(
            <BrowserRouter>
                <DevQA />
            </BrowserRouter>
        );

        await waitFor(() => {
            expect(screen.getByText('Test Quest 1')).toBeInTheDocument();
        });

        // Select "Foundry" in world filter
        const worldSelect = screen.getByDisplayValue('All Worlds');
        fireEvent.change(worldSelect, { target: { value: 'foundry' } });

        await waitFor(() => {
            expect(getQAQuests).toHaveBeenCalledWith(
                expect.objectContaining({ world_id: 'foundry' })
            );
        });
    });

    it('shows error state when API fails', async () => {
        (getQASummary as any).mockRejectedValue(new Error('API Error'));
        (getQAQuests as any).mockRejectedValue(new Error('API Error'));

        render(
            <BrowserRouter>
                <DevQA />
            </BrowserRouter>
        );

        await waitFor(() => {
            expect(screen.getByText(/Failed to load QA data/i)).toBeInTheDocument();
        });

        expect(screen.getByText('Retry')).toBeInTheDocument();
    });
});

describe('DevQA Integrity Flow', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        (getQASummary as any).mockResolvedValue(mockSummary);
        (getQAQuests as any).mockResolvedValue(mockQuests);
    });

    it('runs integrity check and shows results modal', async () => {
        const mockRunResponse = { run_id: 'qarun_test123', status: 'queued' };
        const mockRunResult = {
            id: 'qarun_test123',
            quest_slug: 'quest-test-1',
            variant: 'integrity',
            status: 'finished',
            duration_ms: 1234,
            result: {
                passed: true,
                issues: [],
            },
            logs: 'Test completed successfully',
            diagnostics: {},
            test_summary: {},
            created_at: '2026-01-31T12:00:00Z',
        };

        (runQATest as any).mockResolvedValue(mockRunResponse);
        (pollQARun as any).mockImplementation((runId, onUpdate) => {
            // Simulate polling by calling onUpdate with final result
            onUpdate(mockRunResult);
            return Promise.resolve(mockRunResult);
        });

        render(
            <BrowserRouter>
                <DevQA />
            </BrowserRouter>
        );

        await waitFor(() => {
            expect(screen.getByText('Test Quest 1')).toBeInTheDocument();
        });

        // Click "Integrity" button for first quest
        const integrityButtons = screen.getAllByText('Integrity');
        fireEvent.click(integrityButtons[0]);

        // Verify runQATest was called
        await waitFor(() => {
            expect(runQATest).toHaveBeenCalledWith({
                quest_id: 'quest-test-1',
                variant: 'integrity',
            });
        });

        // Verify polling was initiated
        expect(pollQARun).toHaveBeenCalled();

        // Verify results modal appears with PASSED status
        await waitFor(() => {
            expect(screen.getByText('PASSED')).toBeInTheDocument();
        });

        expect(screen.getByText('INTEGRITY Test Results')).toBeInTheDocument();
        expect(screen.getByText(/Duration: 1234ms/i)).toBeInTheDocument();
    });

    it('shows failed integrity check with issues', async () => {
        const mockRunResponse = { run_id: 'qarun_fail123', status: 'queued' };
        const mockFailedResult = {
            id: 'qarun_fail123',
            quest_slug: 'quest-test-2',
            variant: 'integrity',
            status: 'finished',
            duration_ms: 2000,
            result: {
                passed: false,
                issues: ['Starter code PASSED but should FAIL', 'Solution code FAILED but should PASS'],
            },
            logs: 'Test failed',
            diagnostics: {},
            test_summary: {},
            created_at: '2026-01-31T12:00:00Z',
        };

        (runQATest as any).mockResolvedValue(mockRunResponse);
        (pollQARun as any).mockImplementation((runId, onUpdate) => {
            onUpdate(mockFailedResult);
            return Promise.resolve(mockFailedResult);
        });

        render(
            <BrowserRouter>
                <DevQA />
            </BrowserRouter>
        );

        await waitFor(() => {
            expect(screen.getByText('Test Quest 2')).toBeInTheDocument();
        });

        const integrityButtons = screen.getAllByText('Integrity');
        fireEvent.click(integrityButtons[1]);

        await waitFor(() => {
            expect(screen.getByText('FAILED')).toBeInTheDocument();
        });

        // Verify issues are displayed
        expect(screen.getByText('Issues Found:')).toBeInTheDocument();
        expect(screen.getByText(/Starter code PASSED but should FAIL/i)).toBeInTheDocument();
        expect(screen.getByText(/Solution code FAILED but should PASS/i)).toBeInTheDocument();
    });

    it('shows running state during test execution', async () => {
        const mockRunResponse = { run_id: 'qarun_running', status: 'queued' };

        (runQATest as any).mockResolvedValue(mockRunResponse);
        (pollQARun as any).mockImplementation(() => {
            // Simulate long-running test
            return new Promise((resolve) => setTimeout(resolve, 10000));
        });

        render(
            <BrowserRouter>
                <DevQA />
            </BrowserRouter>
        );

        await waitFor(() => {
            expect(screen.getByText('Test Quest 1')).toBeInTheDocument();
        });

        const integrityButtons = screen.getAllByText('Integrity');
        fireEvent.click(integrityButtons[0]);

        // Verify "Running..." state appears
        await waitFor(() => {
            expect(screen.getByText('Running...')).toBeInTheDocument();
        });
    });
});
