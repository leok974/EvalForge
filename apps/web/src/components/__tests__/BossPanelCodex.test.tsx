import { render, screen, fireEvent } from '@testing-library/react';
import { BossPanel } from '../BossPanel';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import { useBossStore } from '@/store/bossStore';

// Mock gameStore
vi.mock('@/store/gameStore', () => ({
    useGameStore: () => ({
        damageIntegrity: vi.fn(),
        addXp: vi.fn(),
    }),
}));

// Mock fetch
global.fetch = vi.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve({ active: false }),
    })
) as any;

describe('BossPanel', () => {
    beforeEach(() => {
        useBossStore.setState({
            status: 'active',
            bossId: 'reactor_core',
            encounterId: 123,
            setBossResolved: vi.fn(),
        });
    });

    it('renders Open Boss Intel button and calls onOpenCodex', () => {
        const onOpenCodex = vi.fn();
        render(<BossPanel onOpenCodex={onOpenCodex} />);

        const button = screen.getByText(/Open Boss Intel/i);
        expect(button).toBeTruthy();

        fireEvent.click(button);
        expect(onOpenCodex).toHaveBeenCalled();
    });
});
