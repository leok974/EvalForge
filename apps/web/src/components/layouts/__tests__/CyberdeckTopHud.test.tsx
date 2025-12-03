import { describe, it, expect } from 'vitest';
import { render, screen } from "@testing-library/react";
import { CyberdeckTopHud } from "../CyberdeckTopHud";

describe("CyberdeckTopHud", () => {
    it("renders XP bar, level, and active quest", () => {
        render(
            <CyberdeckTopHud
                level={7}
                xp={450}
                xpToNext={900}
                systemIntegrity={92}
                activeQuest="PYTHON – BOSS FIGHT"
                worldLabel="PYTHON WORLD – FUNDAMENTALS"
                latencyMs={42}
                secure={true}
                online={true}
            />
        );

        expect(screen.getByText(/level/i)).toBeInTheDocument();
        expect(screen.getByText("PYTHON – BOSS FIGHT")).toBeInTheDocument();
        expect(screen.getByText(/92%/)).toBeInTheDocument();
        expect(screen.getByText(/42ms/)).toBeInTheDocument();
    });
});
