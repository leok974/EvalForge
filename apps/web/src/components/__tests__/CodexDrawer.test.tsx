import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { CodexDrawer } from '../CodexDrawer';

// Mock Fetch
global.fetch = vi.fn();

// Mock Syntax Highlighter (It's heavy and breaks in JSDOM sometimes)
vi.mock('react-syntax-highlighter', () => ({
    Prism: ({ children }: any) => <pre data-testid="code-block">{children}</pre>
}));

// Mock Game Store
vi.mock('../../store/gameStore', () => ({
    useGameStore: () => (() => { }) // Mock addXp function
}));

describe('CodexDrawer (Holocron Update)', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    const mockEntry = {
        metadata: { id: 'doc1', title: 'Advanced Patterns', tags: ['architecture'], world: 'python' },
        content: "# Intro\n\n```python\nprint('Hello')\n```"
    };

    it('renders "Ask Mentor" button when entry is loaded', async () => {
        // 1. Mock Index Response
        (global.fetch as any).mockResolvedValueOnce({
            json: async () => [mockEntry.metadata]
        });

        // 2. Mock Detail Response
        (global.fetch as any).mockResolvedValueOnce({
            json: async () => mockEntry
        });

        render(<CodexDrawer isOpen={true} onClose={() => { }} currentWorldId="python" />);

        // Click item in list
        await waitFor(() => screen.getByText('Advanced Patterns'));
        fireEvent.click(screen.getByText('Advanced Patterns'));

        // 3. Verify Detail View Elements
        await waitFor(() => {
            // Check for the new Action Button
            expect(screen.getByText(/ASK MENTOR/i)).toBeDefined();

            // Check for Syntax Highlighting Mock
            expect(screen.getByTestId('code-block')).toBeDefined();
            expect(screen.getByText("print('Hello')")).toBeDefined();
        });
    });

    it('handles "Ask Mentor" click', async () => {
        // Setup same as above...
        (global.fetch as any).mockResolvedValueOnce({ json: async () => [mockEntry.metadata] });
        (global.fetch as any).mockResolvedValueOnce({ json: async () => mockEntry });

        const handleClose = vi.fn();
        render(<CodexDrawer isOpen={true} onClose={handleClose} currentWorldId="python" />);

        await waitFor(() => screen.getByText('Advanced Patterns'));
        fireEvent.click(screen.getByText('Advanced Patterns'));

        await waitFor(() => screen.getByText(/ASK MENTOR/i));

        // Test Click
        fireEvent.click(screen.getByText(/ASK MENTOR/i));

        // Should close the drawer (to reveal chat)
        // In a real integration test, we'd check if it updated the chat input too
        expect(handleClose).toHaveBeenCalled();
    });
});
