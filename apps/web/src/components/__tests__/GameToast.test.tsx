import { render, screen } from '@testing-library/react';
import { GameToast } from '../GameToast';
import * as HookModule from '../../hooks/useGameSocket';
import { vi, describe, it, expect } from 'vitest';

// Mock the hook
vi.mock('../../hooks/useGameSocket', () => ({
    useGameSocket: vi.fn()
}));

describe('GameToast Component', () => {
    it('renders nothing when no event', () => {
        (HookModule.useGameSocket as any).mockReturnValue(null);
        const { container } = render(<GameToast />);
        expect(container.firstChild).toBeNull();
    });

    it('renders Achievement events with Gold styling', () => {
        const { rerender } = render(<GameToast />);

        // Simulate Achievement Event
        (HookModule.useGameSocket as any).mockReturnValue({
            type: 'achievement',
            badge: {
                name: 'MASTER ARCHITECT',
                description: 'Built a massive system.',
                icon: '🏛️',
                rarity: 'legendary',
                xp_bonus: 5000
            }
        });

        rerender(<GameToast />);

        // 1. Check Content
        expect(screen.getByText('ACHIEVEMENT UNLOCKED')).toBeDefined();
        expect(screen.getByText('MASTER ARCHITECT')).toBeDefined();
        expect(screen.getByText('Built a massive system.')).toBeDefined();
        expect(screen.getByText('+5000 XP BONUS')).toBeDefined();
        expect(screen.getByText('🏛️')).toBeDefined();

        // 2. Check Styling (Gold/Banana Border)
        // We look for the class directly in the container
        const toast = document.querySelector('.border-banana-400');
        expect(toast).not.toBeNull();
    });
});
