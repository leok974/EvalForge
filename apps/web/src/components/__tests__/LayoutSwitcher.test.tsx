import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { LayoutSwitcher } from '../LayoutSwitcher';
import { useGameStore } from '../../store/gameStore';

// Mock the hooks directly
vi.mock('../../features/layouts/useLayoutUnlocks', () => ({
  useLayoutUnlocks: vi.fn()
}));

vi.mock('../../hooks/useCurrentLayout', () => ({
  useCurrentLayout: () => ({ layout: 'cyberdeck', setLayout: vi.fn() })
}));

import { useLayoutUnlocks } from '../../features/layouts/useLayoutUnlocks';

describe("LayoutSwitcher", () => {
  it("shows Orion option when unlocked", () => {
    // Mock the hook to return unlocked Orion
    (useLayoutUnlocks as any).mockReturnValue([
      { id: 'cyberdeck', label: 'Cyberdeck', unlocked: true },
      { id: 'orion', label: 'Orion', unlocked: true, description: 'Star Map' }
    ]);

    render(<LayoutSwitcher />);

    fireEvent.click(screen.getByTestId('layout-picker-trigger'));
    expect(screen.getByText(/Star Map/i)).toBeInTheDocument();
    expect(screen.getByTestId('layout-option-orion')).not.toBeDisabled();
  });

  it("shows Orion as disabled/locked when locked", () => {
    // Mock the hook to return locked Orion
    (useLayoutUnlocks as any).mockReturnValue([
      { id: 'cyberdeck', label: 'Cyberdeck', unlocked: true },
      { id: 'orion', label: 'Orion', unlocked: false, description: 'Star Map', lockedReason: 'Need Level 3' }
    ]);

    render(<LayoutSwitcher />);

    fireEvent.click(screen.getByTestId('layout-picker-trigger'));

    const option = screen.getByTestId('layout-option-orion');
    expect(option).toBeDisabled();
    expect(screen.getByText('Need Level 3')).toBeInTheDocument();
  });
});
