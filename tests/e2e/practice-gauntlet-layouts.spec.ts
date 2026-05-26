import { test, expect } from "@playwright/test";

/**
 * E2E guard: Practice Gauntlet appears in Workshop layout.
 *
 * Sprint 22: CyberdeckLayout deleted. /deck now redirects to /arcade/workshop.
 * The Cyberdeck test is removed — the layout no longer exists.
 * Only Workshop needs to be verified.
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

    // Cyberdeck test DELETED Sprint 22: CyberdeckLayout (apps/web/src/layouts/CyberdeckLayout.tsx)
    // was deleted. /deck now redirects to /arcade/workshop.
    // Orion layout test DELETED Sprint 15: OrionLayout does not mount PracticeGauntletCard.

});
