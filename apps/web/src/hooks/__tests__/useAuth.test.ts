import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useAuth } from '../useAuth';

// Mock global fetch
global.fetch = vi.fn();

const mockUser = {
    id: 'leo',
    name: 'Leo (Dev)',
    avatar_url: 'http://avatar.url',
    auth_mode: 'mock'
};

describe('useAuth Hook', () => {
    beforeEach(() => {
        vi.resetAllMocks();
    });

    it('fetches user on mount', async () => {
        // Mock successful /api/auth/me response
        (global.fetch as any).mockResolvedValueOnce({
            ok: true,
            json: async () => mockUser,
        });

        const { result } = renderHook(() => useAuth());

        // Initially loading
        expect(result.current.loading).toBe(true);

        // Wait for fetch
        await waitFor(() => {
            expect(result.current.loading).toBe(false);
        });

        expect(result.current.user).toEqual(mockUser);
        expect(global.fetch).toHaveBeenCalledWith('/api/auth/me');
    });

    it('handles login flow (Mock)', async () => {
        // 1. Initial State (Logged out)
        (global.fetch as any).mockResolvedValueOnce({
            ok: true,
            json: async () => ({}), // Empty object = not logged in
        });

        const { result } = renderHook(() => useAuth());
        await waitFor(() => expect(result.current.loading).toBe(false));
        expect(result.current.user).toBeNull();

        // 2. Mock window.location.href to prevent actual navigation
        delete (window as any).location;
        (window as any).location = { href: '' };

        // 3. Mock login endpoint to return redirect URL
        (global.fetch as any).mockResolvedValueOnce({
            ok: true,
            json: async () => ({ url: 'https://github.com/login/oauth/authorize' })
        });

        // 4. Trigger Login
        result.current.login();

        // 5. Wait for redirect URL to be set
        await waitFor(() => {
            expect((window as any).location.href).toBe('https://github.com/login/oauth/authorize');
        });

        expect(global.fetch).toHaveBeenCalledWith('/api/auth/github/start');
    });

    it('handles logout', async () => {
        // Setup logged in state
        (global.fetch as any).mockResolvedValueOnce({
            ok: true,
            json: async () => mockUser,
        });
        const { result } = renderHook(() => useAuth());
        await waitFor(() => expect(result.current.user).not.toBeNull());

        // Logout
        result.current.logout();
        await waitFor(() => {
            expect(result.current.user).toBeNull();
        });
    });
});
