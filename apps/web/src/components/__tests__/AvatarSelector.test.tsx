import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AvatarSelector } from '../AvatarSelector';

// Mock fetch
window.fetch = vi.fn();

describe('AvatarSelector', () => {
    beforeEach(() => {
        vi.resetAllMocks();
    });

    const mockAvatars = [
        {
            id: 'default_user',
            name: 'Initiate',
            description: 'Basic',
            required_level: 1,
            rarity: 'common',
            visual_type: 'icon',
            visual_data: 'user',
            is_locked: false,
            is_equipped: true
        },
        {
            id: 'neon_ghost',
            name: 'Netrunner',
            description: 'Cool',
            required_level: 10,
            rarity: 'epic',
            visual_type: 'css',
            visual_data: 'neon-pulse',
            is_locked: true,
            is_equipped: false
        }
    ];

    it('renders nothing when closed', () => {
        render(<AvatarSelector isOpen={false} onClose={vi.fn()} />);
        expect(screen.queryByText('AVATAR CLOSET')).toBeNull();
    });

    it('fetches and displays avatars when open', async () => {
        (window.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => ({ avatars: mockAvatars })
        });

        render(<AvatarSelector isOpen={true} onClose={vi.fn()} />);

        // Check loading state
        expect(screen.getByText(/SCANNING/)).toBeDefined();

        // Wait for data
        await waitFor(() => {
            expect(screen.getByText('Initiate')).toBeDefined();
            expect(screen.getByText('Netrunner')).toBeDefined();
        });

        // Check status badges
        expect(screen.getByText('Active')).toBeDefined(); // default_user
        expect(screen.getByText(/Lvl 10/)).toBeDefined(); // neon_ghost lock
    });

    it('handles equip action', async () => {
        (window.fetch as any).mockResolvedValueOnce({
            ok: true,
            json: async () => ({ avatars: mockAvatars })
        });

        render(<AvatarSelector isOpen={true} onClose={vi.fn()} />);

        await waitFor(() => screen.getByText('Initiate'));

        // Mock equip response
        (window.fetch as any).mockResolvedValueOnce({
            ok: true,
            json: async () => ({ status: 'ok', current_avatar_id: 'default_user' })
        });

        // Click the equipped one (just to test the click, logic allows re-equipping)
        fireEvent.click(screen.getByText('Initiate'));

        expect(window.fetch).toHaveBeenCalledTimes(2); // 1 load, 1 equip
        expect(window.fetch).toHaveBeenLastCalledWith('/api/avatars/equip', expect.objectContaining({
            method: 'POST',
            body: JSON.stringify({ avatar_id: 'default_user' })
        }));
    });

    it('disables locked avatars', async () => {
        (window.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => ({ avatars: mockAvatars })
        });

        render(<AvatarSelector isOpen={true} onClose={vi.fn()} />);

        await waitFor(() => screen.getByText('Netrunner'));

        const lockedBtn = screen.getByText('Netrunner').closest('button');
        expect(lockedBtn).toHaveProperty('disabled', true);
    });
});
