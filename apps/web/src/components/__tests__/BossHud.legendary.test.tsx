import { render, screen } from "@testing-library/react";
import { BossHud } from "../../components/BossHud";
import { useBossStore } from "../../store/bossStore";
import { vi, describe, it, expect, Mock } from "vitest";

// Mock the store
vi.mock("../../store/bossStore");
vi.mock("../../store/gameStore", () => ({ useGameStore: (selector: any) => selector({ layout: "workshop", bossesUnlocked: ["b1"] }) }));
vi.mock("../../store/agentStore", () => ({ useAgentStore: () => ({ openAgent: vi.fn() }) }));

describe("BossHud Legendary Visuals", () => {
    it("renders LEGENDARY badge for legendary difficulty", () => {
        (useBossStore as unknown as Mock).mockReturnValue({
            activeBossId: "boss-legendary",
            bossName: "Legendary Boss",
            difficulty: "legendary",
            status: "active",
            integrityCurrent: 100,
            integrityMax: 100,
            bossHpCurrent: 100,
            bossHpMax: 100,
        });

        render(<BossHud />);

        const badge = screen.getByTestId("boss-hud-legendary-badge");
        expect(badge).toBeInTheDocument();
        expect(badge).toHaveTextContent("LEGENDARY");
        expect(badge.className).toContain("amber-900");
    });

    it("does not render LEGENDARY badge for normal difficulty", () => {
        (useBossStore as unknown as jest.Mock).mockReturnValue({
            activeBossId: "boss-normal",
            bossName: "Normal Boss",
            difficulty: "hard",
            status: "active",
            integrityCurrent: 100,
            integrityMax: 100,
            bossHpCurrent: 100,
            bossHpMax: 100,
        });

        render(<BossHud />);

        const badge = screen.queryByTestId("boss-hud-legendary-badge");
        expect(badge).not.toBeInTheDocument();
    });
});
