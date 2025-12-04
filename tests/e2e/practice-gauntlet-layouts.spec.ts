import { test, expect } from "@playwright/test";

/**
 * E2E guard: Practice Gauntlet appears on all key layouts
 * 
 * This ensures we never forget to mount the Practice Gauntlet
 * on any major layout surface.
 */

const routes = [
    { path: "/workshop", label: "Workshop" },
    { path: "/orion", label: "Orion" },
    { path: "/cyberdeck", label: "Cyberdeck" },
];

test.describe("Practice Gauntlet - Layout Consistency", () => {
    for (const { path, label } of routes) {
        test(`Practice Gauntlet appears on ${label} layout`, async ({ page }) => {
            // Navigate to the layout
            await page.goto(path);
            await page.waitForLoadState("networkidle");

            // Check that Practice Gauntlet card is visible
            const card = page.getByTestId("practice-gauntlet-card");
            await expect(card).toBeVisible({ timeout: 10000 });

            // Verify header text
            const header = card.getByText(/Practice Gauntlet/i);
            await expect(header).toBeVisible();
        });
    }

    test("Practice Gauntlet has consistent structure across layouts", async ({ page }) => {
        for (const { path } of routes) {
            await page.goto(path);
            await page.waitForLoadState("networkidle");

            const card = page.getByTestId("practice-gauntlet-card");

            // Should have footer with status
            const footer = card.locator("footer");
            await expect(footer).toBeVisible();

            // Should show either loading, error, empty, or items
            const hasContent = await Promise.race([
                card.getByTestId("practice-gauntlet-loading").isVisible().catch(() => false),
                card.getByTestId("practice-gauntlet-error").isVisible().catch(() => false),
                card.getByTestId("practice-gauntlet-empty").isVisible().catch(() => false),
                card.getByTestId("practice-gauntlet-items").isVisible().catch(() => false),
            ]);

            expect(hasContent).toBeTruthy();
        }
    });
});
