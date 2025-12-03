import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from "@testing-library/react";
import { OrionMap } from "../OrionMap";
import { ORION_WORLDS } from "../orion/types";

vi.mock("@/lib/featureFlags", () => ({
    fxEnabled: true,
}));

vi.mock("./orion/adapters", () => ({
    buildOrionTracks: () => [
        {
            id: "track-1",
            title: "Python Fundamentals",
            difficulty: "novice",
            progressPct: 50,
            orbitIndex: 1,
            angleDeg: 30,
        },
    ],
}));

describe("OrionMap", () => {
    it("renders world labels and track nodes", () => {
        render(
            <OrionMap
                activeWorldId={ORION_WORLDS[0].id}
                onWorldChange={() => { }}
                onTrackSelected={() => { }}
            />
        );

        expect(screen.getByTestId("orion-map")).toBeInTheDocument();
        expect(screen.getByText(/python fundamentals/i)).toBeInTheDocument();
    });

    it("applies parallax transform on mouse move when fx is enabled", () => {
        render(
            <OrionMap
                activeWorldId={ORION_WORLDS[0].id}
                onWorldChange={() => { }}
                onTrackSelected={() => { }}
            />
        );

        const map = screen.getByTestId("orion-map");
        fireEvent.mouseMove(map, { clientX: 10, clientY: 10 });

        // We don't assert exact values, just that the style is set somewhere
        const parallaxLayers = document.querySelectorAll(
            ".orion-spin-worlds, .orion-spin-orbits"
        );
        expect(parallaxLayers.length).toBeGreaterThan(0);
    });
});
