import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ProjectsPanel } from '../ProjectsPanel';

global.fetch = vi.fn();

const mockUser = {
    id: 'leo',
    name: 'Leo',
    avatar_url: '',
    auth_mode: 'mock'
};

const mockProject = {
    id: 'p1',
    name: 'my-repo',
    repo_url: 'http://github.com/u/my-repo',
    sync_status: 'ok',
    last_sync_at: '2025-01-01',
    summary_data: { stack: ['react'] }
};

describe('ProjectsPanel', () => {
    beforeEach(() => {
        vi.resetAllMocks();
    });

    it('does not render when closed', () => {
        render(<ProjectsPanel user={mockUser} isOpen={false} onClose={() => { }} />);
        expect(screen.queryByText('PROJECT DASHBOARD')).toBeNull();
    });

    it('renders list of projects when open', async () => {
        (global.fetch as any).mockResolvedValueOnce({
            json: async () => [mockProject]
        });

        render(<ProjectsPanel user={mockUser} isOpen={true} onClose={() => { }} />);

        expect(global.fetch).toHaveBeenCalledWith('/api/projects');
        await waitFor(() => {
            expect(screen.getByText('my-repo')).toBeDefined();
            // Use a more flexible matcher for the stack tag
            expect(screen.getByText((content, element) => {
                return element?.tagName.toLowerCase() === 'span' && content.includes('react');
            })).toBeDefined();
        });
    });

    it('handles adding a new project', async () => {
        // 1. Initial Load (Empty)
        (global.fetch as any).mockResolvedValueOnce({ json: async () => [] });

        render(<ProjectsPanel user={mockUser} isOpen={true} onClose={() => { }} />);

        // 2. Setup Mocks for Add Flow
        // POST /api/projects -> returns new ID
        (global.fetch as any).mockResolvedValueOnce({ ok: true, json: async () => ({ id: 'new-p2' }) });
        // POST /sync -> returns success
        (global.fetch as any).mockResolvedValueOnce({ ok: true });
        // GET /api/projects (Refresh) -> returns new list
        (global.fetch as any).mockResolvedValueOnce({
            ok: true,
            json: async () => [mockProject, { ...mockProject, id: 'new-p2', name: 'new-repo' }]
        });

        // 3. User Interaction
        const input = screen.getByPlaceholderText('https://github.com/username/repo');
        fireEvent.change(input, { target: { value: 'https://github.com/u/new-repo' } });

        const btn = screen.getByText('ADD PROJECT');
        fireEvent.click(btn);

        // 4. Verification
        await waitFor(() => {
            expect(screen.getByText('ADD PROJECT')).toBeDefined(); // Button resets
        });

        // Check API Chain - Order matters!
        // 1. Initial load
        expect(global.fetch).toHaveBeenNthCalledWith(1, '/api/projects');
        // 2. Add Project
        expect(global.fetch).toHaveBeenNthCalledWith(2, '/api/projects', expect.objectContaining({
            method: 'POST',
            body: JSON.stringify({ repo_url: 'https://github.com/u/new-repo' })
        }));
        // 3. Sync
        expect(global.fetch).toHaveBeenNthCalledWith(3, '/api/projects/new-p2/sync', expect.objectContaining({ method: 'POST' }));
        // 4. Refresh list
        expect(global.fetch).toHaveBeenNthCalledWith(4, '/api/projects');

        // Check UI Update
        await waitFor(() => expect(screen.getByText('new-repo')).toBeDefined());
    });
});
