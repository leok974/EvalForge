// apps/web/src/components/devtools/__tests__/IntentOracleEvalButton.meta.test.tsx

import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';

import { IntentOracleEvalButton } from "../IntentOracleEvalButton";

describe("IntentOracleEvalButton – combat summary", () => {
    beforeEach(() => {
        // @ts-ignore
        global.fetch = vi.fn();
    });

    afterEach(() => {
        vi.resetAllMocks();
    });

    it("renders Integrity and Boss HP deltas when meta fields are present", async () => {
        (global.fetch as any).mockResolvedValueOnce({
            ok: true,
            json: async () => ({
                success: true,
                score: 0.9,
                integrity_before: 100,
                integrity_after: 85,
                integrity_delta: -15,
                boss_hp_before: 100,
                boss_hp_after: 40,
                boss_hp_delta: -60,
            }),
            text: async () => "",
        });

        render(
            <IntentOracleEvalButton endpoint="/api/agents/intent-oracle/eval" />
        );

        const btn = screen.getByRole("button", { name: /run eval/i });
        fireEvent.click(btn);

        const meta = await screen.findByTestId("intent-oracle-eval-meta");
        expect(meta.textContent).toMatch(/Integrity/i);
        expect(meta.textContent).toMatch(/100/);
        expect(meta.textContent).toMatch(/85/);
        expect(meta.textContent).toMatch(/\(-15\)/);

        expect(meta.textContent).toMatch(/Boss HP/i);
        expect(meta.textContent).toMatch(/40/);
        expect(meta.textContent).toMatch(/\(-60\)/);
    });

    it("does not render combat summary when meta fields are missing", async () => {
        (global.fetch as any).mockResolvedValueOnce({
            ok: true,
            json: async () => ({
                success: true,
                score: 0.9,
            }),
            text: async () => "",
        });

        render(
            <IntentOracleEvalButton endpoint="/api/agents/intent-oracle/eval" />
        );

        const btn = screen.getByRole("button", { name: /run eval/i });
        fireEvent.click(btn);

        await waitFor(() => {
            expect(
                screen.queryByTestId("intent-oracle-eval-meta")
            ).toBeNull();
        });
    });
});
