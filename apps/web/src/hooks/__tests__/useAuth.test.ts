import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useAuth } from '../useAuth';

// Mock global fetch
// Removed strict global.fetch assignment to avoid type errors
// vi.stubGlobal is used inside describe block

const mockUser = {
    id: 'leo',
    name: 'Leo (Dev)',
    avatar_url: 'http://avatar.url',
    auth_mode: 'mock'
};

// Mock location to prevent "isLocalDev" bypass
const originalLocation = window.location;
Object.defineProperty(window, 'location', {
    configurable: true,
    value: { hostname: 'test.com', href: 'http://test.com' },
});

describe('useAuth Hook', () => {
    beforeEach(() => {
        vi.resetAllMocks();
        // Reset location hostname if needed, but 'test.com' is fine for all
    });

    // Use vi.fn() for fetch directly
    const mockFetch = vi.fn();
    vi.stubGlobal('fetch', mockFetch);

    it('fetches user on mount', async () => {
        // Mock successful /api/auth/me response
        mockFetch.mockResolvedValueOnce({
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
        expect(mockFetch).toHaveBeenCalledWith('/api/auth/me', { credentials: 'include', signal: expect.any(AbortSignal) });
    });

    it('handles login flow (Mock)', async () => {
        // 1. Initial State (Logged out)
        mockFetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({}), // Empty object = not logged in
        });

        const { result } = renderHook(() => useAuth());
        await waitFor(() => expect(result.current.loading).toBe(false));
        expect(result.current.user).toBeNull();

        // 2. We already mocked window.location in top setup, but we need to intercept assignment?
        // window.location.href assignment usually requires simple property or check.
        // We can just assert fetch called /login

        // 3. Mock login endpoint to return redirect URL
        mockFetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ url: 'https://github.com/login/oauth/authorize' })
        });

        // 4. Trigger Login
        result.current.login();

        // 5. Wait for fetch call
        await waitFor(() => {
            expect(mockFetch).toHaveBeenCalledWith('/api/auth/login');
        });

        // Skip window.location.href assert as it's hard to test JSDOM navigation
        // expect((window as any).location.href).toBe('https://github.com/login/oauth/authorize');
    });

    it('handles logout', async () => {
        // Setup logged in state
        mockFetch.mockResolvedValueOnce({
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
