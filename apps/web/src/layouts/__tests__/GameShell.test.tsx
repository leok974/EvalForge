import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { GameShell } from '../GameShell';
import { useGameStore } from '../../store/gameStore';

// Mock DevUI to avoid rendering the full application tree
vi.mock('../../pages/DevUI', () => ({
  default: () => <div data-testid="dev-ui-mock">DevUI Rendered</div>
}));

// Mock child layouts (even though they shouldn't be rendered directly anymore, good for safety)
vi.mock('../CyberdeckLayout', () => ({
  CyberdeckLayout: () => <div data-testid="layout-cyberdeck">Cyberdeck Rendered</div>
}));

describe('GameShell', () => {
  it('renders DevUI which initializes correctly', () => {
    useGameStore.setState({ layout: 'cyberdeck' });
    render(<GameShell />);
    expect(screen.getByTestId('dev-ui-mock')).toBeDefined();
  });
});
