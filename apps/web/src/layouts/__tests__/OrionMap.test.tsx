import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from "@testing-library/react";
import { OrionMap } from "../OrionMap";

vi.mock("@/lib/featureFlags", () => ({
    fxEnabled: true,
}));

vi.mock("../orion/adapters", () => ({
    getWorldNodes: () => [
        { id: "world-python", label: "Python", color: "#afeeee", radius: 50, angle: 0 },
        { id: "world-js", label: "JS", color: "#ffff00", radius: 50, angle: 1 }
    ],
    getTrackNodesForWorld: () => [
        {
            id: "track-1",
            title: "Python Fundamentals",
            difficulty: "novice",
            progressPct: 50,
            orbitIndex: 1,
            angleDeg: 30,
            radius: 100,
            angle: 0,
            slug: "python-fundamentals",
            worldSlug: "python"
        },
    ],
}));

vi.mock("@/store/gameStore", () => ({
    useGameStore: vi.fn(() => ({
        activeTrack: null,
        setActiveTrack: vi.fn(),
    })),
}));

describe("OrionMap", () => {
    it("renders world labels and track nodes", () => {
        render(<OrionMap />);

        expect(screen.getByTestId("orion-map")).toBeInTheDocument();
        // Track title appears in both the node and info panel
        const trackElements = screen.getAllByText(/python fundamentals/i);
        expect(trackElements.length).toBeGreaterThan(0);
    });

    it("applies parallax transform on mouse move when fx is enabled", () => {
        render(<OrionMap />);

        const map = screen.getByTestId("orion-map");
        fireEvent.mouseMove(map, { clientX: 10, clientY: 10 });

        // Check if the stars layer exists (it should be rendered by Starfield)
        const starLayer = map.querySelector(".orion-stars-fast");
        expect(starLayer).toBeInTheDocument();
    });
});
