import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AvatarSelector } from '../AvatarSelector';
import * as AuthHook from '../../hooks/useAuth';

// Mock dependencies
global.fetch = vi.fn();
vi.mock('../../hooks/useAuth', () => ({
    useAuth: vi.fn()
}));

const mockAvatars = [
    { id: 'av1', name: 'Starter', is_locked: false, is_equipped: true, required_level: 1, visual_type: 'icon' },
    { id: 'av2', name: 'Advanced', is_locked: true, is_equipped: false, required_level: 50, visual_type: 'icon' }
];

describe('AvatarSelector', () => {
    beforeEach(() => {
        vi.resetAllMocks();
        (AuthHook.useAuth as any).mockReturnValue({
            user: { id: 'leo' },
            refresh: vi.fn()
        });
    });

    it('renders the grid correctly', async () => {
        (global.fetch as any).mockResolvedValueOnce({
            json: async () => mockAvatars
        });

        render(<AvatarSelector isOpen={true} onClose={() => { }} />);

        // Wait for load
        await waitFor(() => screen.getByText('Starter'));

        // Check states
        expect(screen.getByText('EQUIPPED')).toBeDefined(); // For av1
        expect(screen.getByText('🔒 LVL 50')).toBeDefined(); // For av2
    });

    it('handles equipping an unlocked avatar', async () => {
        // 1. Initial Load
        const unlockedAvatar = { ...mockAvatars[0], is_equipped: false };
        (global.fetch as any).mockResolvedValueOnce({
            json: async () => [unlockedAvatar]
        });

        // 2. Setup Equip Response
        (global.fetch as any).mockResolvedValueOnce({ ok: true });

        render(<AvatarSelector isOpen={true} onClose={() => { }} />);
        await waitFor(() => screen.getByText('Starter'));

        // 3. Click
        fireEvent.click(screen.getByText('Starter'));

        // 4. Verify API Call
        expect(global.fetch).toHaveBeenCalledWith('/api/avatars/equip', expect.objectContaining({
            method: 'POST',
            body: JSON.stringify({ avatar_id: 'av1' })
        }));
    });

    it('prevents equipping a locked avatar', async () => {
        (global.fetch as any).mockResolvedValueOnce({
            json: async () => [mockAvatars[1]] // The locked one
        });

        render(<AvatarSelector isOpen={true} onClose={() => { }} />);
        await waitFor(() => screen.getByText('Advanced'));

        // Click Locked Item
        const card = screen.getByText('Advanced').closest('div');
        if (card) fireEvent.click(card);

        // Verify NO equip call was made (fetch only called once for listing)
        expect(global.fetch).toHaveBeenCalledTimes(1);
    });
});
