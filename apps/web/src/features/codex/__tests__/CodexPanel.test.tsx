
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { CodexPanel } from '../CodexPanel';
import React from 'react';
import * as useOpenCodex from '../../../hooks/useOpenCodex';

// Mock APIs to avoid alias issues and isolate tests
vi.mock('../../../lib/questsApi', () => ({
    fetchQuest: vi.fn(),
}));

vi.mock('../../../lib/codexApi', () => ({
    fetchCodex: vi.fn(),
    fetchCodexIndex: vi.fn(),
}));

// Import mocked modules
import { fetchQuest } from '../../../lib/questsApi';
import { fetchCodex, fetchCodexIndex } from '../../../lib/codexApi';

// Mock lucide icons
vi.mock('lucide-react', () => ({
    BookOpen: () => <div data-testid="icon-book" />,
    Search: () => <div data-testid="icon-search" />,
    History: () => <div data-testid="icon-history" />,
    Bookmark: () => <div data-testid="icon-bookmark" />,
    ArrowLeft: () => <div data-testid="icon-back" />,
    Filter: () => <div data-testid="icon-filter" />,
    Globe: () => <div data-testid="icon-globe" />
}));

// Mock CodexMarkdown to avoid complex rendering in panel tests
vi.mock('../CodexMarkdown', () => ({
    CodexMarkdown: ({ markdown, overrideTitle }: any) => (
        <div data-testid="codex-markdown">
            <h1>{overrideTitle || 'No Title'}</h1>
            <div>{markdown}</div>
        </div>
    )
}));

describe('CodexPanel', () => {
    beforeEach(() => {
        localStorage.clear();
        vi.clearAllMocks();

        // Mock hooks
        vi.spyOn(useOpenCodex, 'useOpenCodex').mockReturnValue(vi.fn());

        // Default Mocks
        (fetchCodexIndex as any).mockResolvedValue({
            sections: [
                {
                    world: 'python',
                    section: 'basics',
                    pages: [
                        { id: '1', title: 'Python Intro', world: 'python', section: 'basics' }
                    ]
                }
            ]
        });

        (fetchQuest as any).mockResolvedValue({
            id: 1,
            slug: 'test-quest',
            key_terms: [
                { id: 't1', term: 'Variable', codex_ref: 'codex:variable' }
            ]
        });

        (fetchCodex as any).mockResolvedValue({
            ref: 'codex:variable',
            title: 'Variable',
            md: '# Variable Info',
            path: 'variable'
        });
    });

    it('renders search bar and world filters', async () => {
        render(<CodexPanel />);

        await waitFor(() => {
            expect(screen.getByText('python')).toBeInTheDocument();
        });

        expect(screen.getByPlaceholderText('Search Codex...')).toBeInTheDocument();
    });

    it('shows recent terms from local storage', async () => {
        localStorage.setItem('codex_recents', JSON.stringify(['codex:term1', 'codex:term2']));
        render(<CodexPanel />);

        expect(screen.getByText(/Recent/i)).toBeInTheDocument();
        expect(screen.getByText('term1')).toBeInTheDocument();
        expect(screen.getByText('term2')).toBeInTheDocument();
    });

    it('navigates to term detail and renders content', async () => {
        render(<CodexPanel initialTerm="codex:variable" />);

        await waitFor(() => {
            expect(screen.getByTestId('codex-markdown')).toBeInTheDocument();
            expect(screen.getByText('Variable')).toBeInTheDocument(); // Title check
            expect(screen.getByText('# Variable Info')).toBeInTheDocument(); // MD check
        });
    });

    it('fetches and shows quest terms when questSlug is provided', async () => {
        render(<CodexPanel questSlug="test-quest" />);

        await waitFor(() => {
            expect(fetchQuest).toHaveBeenCalledWith('test-quest');
        });

        expect(screen.getByText(/For this Quest/i)).toBeInTheDocument();
        expect(screen.getByText('Variable')).toBeInTheDocument();
    });

    it('filters search results by world', async () => {
        render(<CodexPanel />);

        await waitFor(() => {
            expect(screen.getByText('python')).toBeInTheDocument();
        });

        const input = screen.getByPlaceholderText('Search Codex...');
        fireEvent.change(input, { target: { value: 'Intro' } });

        const pythonPill = screen.getByTestId('codex-world-pill-python');
        fireEvent.click(pythonPill);

        expect(screen.getByText('Python Intro')).toBeInTheDocument();
    });
});
