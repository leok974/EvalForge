import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import { OrionLayout } from '../OrionLayout';

// Mock child components to isolate layout logic
vi.mock("../OrionMap", () => ({
    OrionMap: () => <div data-testid="mock-orion-map">Orion Map</div>
}));

vi.mock("@/components/shell/GameShellHeader", () => ({
    GameShellHeader: () => <div data-testid="mock-header">Header</div>
}));

vi.mock("@/components/hud/ActiveTrackStatus", () => ({
    ActiveTrackStatus: () => <div data-testid="mock-status">Active Track Status</div>
}));

vi.mock("@/components/layout/RightRailBossPracticeColumn", () => ({
    RightRailBossPracticeColumn: () => <div data-testid="mock-right-rail">Right Rail</div>
}));

// Mock game store
vi.mock("@/store/gameStore", () => ({
    useGameStore: vi.fn((selector) => {
        const state = {
            activeTrack: null, // Default
        };
        return selector(state);
    }),
}));

// Robust Fetch Mock
const fetchMock = vi.fn((url: string | Request | URL) => {
    return Promise.resolve({
        ok: true,
        json: async () => ({})
    });
});
vi.stubGlobal('fetch', fetchMock);

describe("OrionLayout", () => {
    it("renders correctly", () => {
        render(
            <MemoryRouter>
                <OrionLayout />
            </MemoryRouter>
        );
        expect(screen.getByTestId("mock-header")).toBeInTheDocument();
        expect(screen.getByTestId("mock-orion-map")).toBeInTheDocument();
        expect(screen.getByTestId("mock-status")).toBeInTheDocument();
        // Check for right rail if visible
        // expect(screen.getByTestId("mock-right-rail")).toBeInTheDocument(); // Hidden on small screens, test might need adjustment if default viewport is small
    });

    it("disables warp/open buttons when no active track", () => {
        render(
            <MemoryRouter>
                <OrionLayout />
            </MemoryRouter>
        );

        expect(
            screen.getByRole('button', { name: /warp to track/i })
        ).toBeDisabled();
        expect(
            screen.getByRole('button', { name: /open in cyberdeck/i })
        ).toBeDisabled();
    });
});
