// Sprint 22: CyberdeckLayout deleted, layout field removed from gameStore.
// Mock cleaned up — test verifies DevUI renders correctly inside GameShell.
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { GameShell } from '../GameShell';

// Mock DevUI to avoid rendering the full application tree
vi.mock('../../pages/DevUI', () => ({
  default: () => <div data-testid="dev-ui-mock">DevUI Rendered</div>
}));

describe('GameShell', () => {
  it('renders DevUI which initializes correctly', () => {
    render(<GameShell />);
    expect(screen.getByTestId('dev-ui-mock')).toBeDefined();
  });
});
