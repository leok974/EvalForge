import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { LayoutSwitcher } from '../LayoutSwitcher';
import { useGameStore } from '../../store/gameStore';

// Mock the layouts constant if needed, but we can rely on the real one if it's simple.
// The user's test setup mocks import.meta.env.

describe("LayoutSwitcher", () => {
  function setup(env: Partial<NodeJS.ProcessEnv> = {}) {
    const oldEnv = import.meta.env;
    // @ts-expect-error: test shim
    import.meta.env = { ...oldEnv, ...env };

    const ui = render(
      <LayoutSwitcher />
    );

    return {
      ...ui,
      restore: () => {
        // @ts-expect-error
        import.meta.env = oldEnv;
      },
    };
  }

  it("shows Orion option when enabled", () => {
    const { restore } = setup({ VITE_LAYOUT_ORION_ENABLED: "1" });

    fireEvent.click(screen.getByText(/layout:/i));
    expect(screen.getByText(/orion map/i)).toBeInTheDocument();

    restore();
  });

  it("does not show Orion option when disabled", () => {
    const { restore } = setup({ VITE_LAYOUT_ORION_ENABLED: "0" });

    fireEvent.click(screen.getByText(/layout:/i));
    expect(screen.queryByText(/orion map/i)).not.toBeInTheDocument();

    restore();
  });
});
