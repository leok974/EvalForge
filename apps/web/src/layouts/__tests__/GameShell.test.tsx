import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { GameShell } from '../GameShell';
import { useGameStore } from '../../store/gameStore';

// Mock the child layouts to avoid rendering the full app tree
vi.mock('../CyberdeckLayout', () => ({
  CyberdeckLayout: () => <div data-testid="layout-cyberdeck">Cyberdeck Rendered</div>
}));

describe('GameShell', () => {
  it('renders Cyberdeck by default', () => {
    useGameStore.setState({ layout: 'cyberdeck' });
    render(<GameShell />);
    expect(screen.getByTestId('layout-cyberdeck')).toBeDefined();
  });

  it('renders Navigator placeholder', () => {
    useGameStore.setState({ layout: 'navigator' });
    render(<GameShell />);
    expect(screen.getByText('NAVIGATOR INTERFACE')).toBeDefined();
  });

  it('renders Workshop placeholder', () => {
    useGameStore.setState({ layout: 'workshop' });
    render(<GameShell />);
    expect(screen.getByText('ISOMETRIC WORKSHOP')).toBeDefined();
  });
});
