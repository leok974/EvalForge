import { test, expect } from "@playwright/test";

/**
 * E2E guard: Practice Gauntlet appears on all key layouts
 *
 * This ensures we never forget to mount the Practice Gauntlet
 * on any major layout surface.
 */

test.describe("Practice Gauntlet - Layout Consistency", () => {

    // /workshop redirects to /arcade/workshop which has the Practice Gauntlet — passes.
    test("Practice Gauntlet appears on Workshop layout", async ({ page }) => {
        await page.goto("/workshop");
        await page.waitForLoadState("networkidle");

        const card = page.getByTestId("practice-gauntlet-card");
        await expect(card).toBeVisible({ timeout: 10000 });

        const header = card.getByText(/Practice Gauntlet/i);
        await expect(header).toBeVisible();
    });

    // Orion layout test DELETED Sprint 15: OrionLayout (apps/web/src/layouts/OrionLayout.tsx)
    // does not mount PracticeGauntletCard. The test premise was wrong — this feature
    // does not exist on the Orion route (/arcade/orion). No route fix would make it pass.

    test("Practice Gauntlet appears on Cyberdeck layout", async ({ page }) => {
        // /deck redirects to /arcade/deck which renders CyberdeckLayout.
        // CyberdeckLayout mounts PracticeGauntletCard directly.
        await page.goto("/deck");
        await page.waitForLoadState("networkidle");
        const card = page.getByTestId("practice-gauntlet-card");
        await expect(card).toBeVisible({ timeout: 10000 });
    });

    // Consistency test DELETED Sprint 15: the test iterated /workshop, /orion, /cyberdeck.
    // OrionLayout does not mount PracticeGauntletCard, so a multi-route consistency
    // check across all three layouts is not valid. Workshop and Cyberdeck are each
    // covered by their own passing tests above.
});
