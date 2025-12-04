// apps/web/tests/e2e/boss-combat.e2e.spec.ts
import { test, expect } from "@playwright/test";

test("Boss HUD updates after a boss submission", async ({ page }) => {
    // 1) Go to whatever screen starts a boss fight.
    // Assuming root or a specific dashboard URL
    await page.goto("/");

    // 2) Start a boss fight: click your "Start Boss" / "Accept" button.
    // Adjust selector to match your actual UI
    // If there's a "Boss Mode" toggle or similar, click that first if needed.
    // For now, looking for a button that might start it.
    const accept = page.getByRole("button", { name: /accept boss|start boss|fight/i });

    // If the button is not visible immediately, we might need to navigate or wait.
    // This is a skeleton, so it might fail if the UI flow is complex.
    if (await accept.isVisible()) {
        await accept.click();
    } else {
        console.log("Accept button not found, skipping click (might already be active)");
    }

    const bossHud = page.getByTestId("boss-hud");
    await expect(bossHud).toBeVisible();

    // Snapshot initial summary text (if any)
    const initialSummary = await bossHud.textContent();

    // 3) Trigger a boss submission – likely via BossPanel's submit button.
    const submit = page.getByRole("button", { name: /submit/i });
    await submit.click();

    // 4) Wait for the combat summary to show deltas
    const summary = page.getByTestId("boss-hud-combat-summary");
    await expect(summary).toBeVisible();

    const summaryText = await summary.textContent();
    expect(summaryText).toMatch(/Integrity/i);
    expect(summaryText).toMatch(/Boss HP/i);

    // Basic regression: the HUD text should not be identical before/after.
    if (initialSummary) {
        expect(summaryText).not.toEqual(initialSummary);
    }
});
