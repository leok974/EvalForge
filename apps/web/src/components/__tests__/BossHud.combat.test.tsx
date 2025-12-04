// apps/web/src/components/__tests__/BossHud.combat.test.tsx

import React from "react";
import { render, screen, act } from "@testing-library/react";
import { describe, it, expect, vi } from 'vitest';

import { BossHud } from "../BossHud";
import { useBossStore } from "../../store/bossStore";

// Mock the store
vi.mock("../../store/bossStore", () => ({
    useBossStore: vi.fn(),
}));

describe("BossHud – combat summary", () => {
    it("shows initial HP/integrity bars and labels", () => {
        // Mock store state
        (useBossStore as any).mockReturnValue({
            activeBossId: "reactor-core",
            bossName: "The Reactor Core",
            status: "active",
            integrityCurrent: 100,
            integrityMax: 100,
            bossHpCurrent: 100,
            bossHpMax: 100,
            deadlineTs: Date.now() + 10000,
        });

        render(<BossHud />);

        expect(screen.getByTestId("boss-hud")).not.toBeNull();
        expect(screen.getByText(/BOSS HP/i)).not.toBeNull();
        expect(screen.getByText(/SYSTEM INTEGRITY/i)).not.toBeNull();
    });

    it("renders before → after deltas when stats change", () => {
        // Initial render
        const mockStore = {
            activeBossId: "reactor-core",
            bossName: "The Reactor Core",
            status: "active",
            integrityCurrent: 100,
            integrityMax: 100,
            bossHpCurrent: 100,
            bossHpMax: 100,
            deadlineTs: Date.now() + 10000,
        };

        (useBossStore as any).mockReturnValue(mockStore);

        const { rerender } = render(<BossHud />);

        // Update stats to simulate damage
        (useBossStore as any).mockReturnValue({
            ...mockStore,
            integrityCurrent: 80,
            bossHpCurrent: 40,
        });

        rerender(<BossHud />);

        const summary = screen.getByTestId("boss-hud-combat-summary");
        const text = summary.textContent ?? "";

        // Integrity: 100 → 80 (-20)
        expect(text).toMatch(/Integrity/i);
        expect(text).toMatch(/100/);
        expect(text).toMatch(/80/);
        expect(text).toMatch(/\(-20\)/);

        // Boss HP: 100 → 40 (-60)
        expect(text).toMatch(/Boss HP/i);
        expect(text).toMatch(/40/);
        expect(text).toMatch(/\(-60\)/);
    });
});
