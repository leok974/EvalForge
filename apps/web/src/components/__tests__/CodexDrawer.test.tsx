import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { CodexDrawer } from '../CodexDrawer';
import React from 'react';

global.fetch = vi.fn();

describe('CodexDrawer', () => {
    it('fetches index when opened', async () => {
        (global.fetch as any).mockResolvedValueOnce({
            json: async () => [{ id: 'doc1', title: 'Doc 1', tags: [] }]
        });

        render(<CodexDrawer isOpen={true} onClose={() => { }} currentWorldId="w1" />);

        expect(global.fetch).toHaveBeenCalledWith('/api/codex?world=w1');
        await waitFor(() => expect(screen.getByText('Doc 1')).toBeDefined());
    });

    it('fetches detail on click', async () => {
        // 1. Index Mock
        (global.fetch as any).mockResolvedValueOnce({
            json: async () => [{ id: 'doc1', title: 'Doc 1', tags: [] }]
        });
        // 2. Detail Mock
        (global.fetch as any).mockResolvedValueOnce({
            json: async () => ({ metadata: { title: 'Doc 1', tags: [] }, content: '# Hello World' })
        });

        render(<CodexDrawer isOpen={true} onClose={() => { }} currentWorldId="w1" />);

        await waitFor(() => screen.getByText('Doc 1'));
        fireEvent.click(screen.getByText('Doc 1'));

        expect(global.fetch).toHaveBeenCalledWith('/api/codex/doc1');
        await waitFor(() => expect(screen.getByText('Hello World')).toBeDefined()); // Markdown rendered
    });
});
