import { render, screen, act } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { FXLayer } from "../FXLayer";
import { useGameSocket } from "../../hooks/useGameSocket";
import { useSettingsStore } from "../../store/settingsStore";

// Mock hooks
vi.mock("../../hooks/useGameSocket");
vi.mock("../../store/settingsStore");
vi.mock("../../store/bossStore", () => ({
    useBossStore: () => ({
        startBoss: vi.fn(),
    }),
}));
vi.mock("../../hooks/useSound", () => ({
    useSound: () => ({ play: vi.fn() }),
}));
vi.mock("../fx/ConfettiManager", () => ({
    ConfettiManager: () => <div data-testid="confetti" />,
}));
vi.mock("../../lib/fx", () => ({
    FX: { emit: vi.fn() },
}));

describe("FXLayer Boss Mechanics", () => {
    it("triggers shake and red tint on boss_spawn", () => {
        // Mock settings
        (useSettingsStore as any).mockReturnValue({ screenShake: true, crtMode: false });

        // Mock socket event
        (useGameSocket as any).mockReturnValue({
            type: "boss_spawn",
            boss_id: "test-boss",
            severity: "high"
        });

        const { container } = render(
            <FXLayer>
                <div>Content</div>
            </FXLayer>
        );

        // Check for tint class
        // Note: The tint is applied via state update which happens in useEffect.
        // We might need to wait or check if render updates.
        // Since we mock the hook return value, the component renders with it immediately?
        // No, useEffect runs after render.

        // We need to re-render or wait for effect?
        // Actually, useGameSocket returns the value, so on first render `lastEvent` is set.
        // useEffect runs, calls setFxState.
        // This triggers re-render.

        // We can check if the class is present.
        // The class is applied to a div.
        const tintLayer = container.querySelector(".deck-boss-tint-red");
        expect(tintLayer).toBeTruthy();

        const shakeLayer = container.querySelector(".deck-boss-shake");
        expect(shakeLayer).toBeTruthy();
    });

    it("triggers green tint on boss success", () => {
        (useSettingsStore as any).mockReturnValue({ screenShake: true });
        (useGameSocket as any).mockReturnValue({
            type: "boss_result",
            outcome: "success"
        });

        const { container } = render(
            <FXLayer>
                <div>Content</div>
            </FXLayer>
        );

        const tintLayer = container.querySelector(".deck-boss-tint-green");
        expect(tintLayer).toBeTruthy();
    });

    it("triggers glitch and red tint on boss failure", () => {
        (useSettingsStore as any).mockReturnValue({ screenShake: true });
        (useGameSocket as any).mockReturnValue({
            type: "boss_result",
            outcome: "failure"
        });

        const { container } = render(
            <FXLayer>
                <div>Content</div>
            </FXLayer>
        );

        const tintLayer = container.querySelector(".deck-boss-tint-red");
        expect(tintLayer).toBeTruthy();

        const glitchLayer = container.querySelector(".deck-boss-glitch");
        expect(glitchLayer).toBeTruthy();
    });
});
