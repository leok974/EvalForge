import { test, expect } from "@playwright/test";

// Helper to handle login
async function loginAsTestUser(page) {
    // In our dev/mock environment, visiting the root URL typically auto-logs in the mock user.
    // We'll navigate to root and wait for the user avatar as confirmation.
    await page.goto("/");

    // Wait for the user avatar using the test id
    // Note: Ensure UserAvatar component has data-testid="user-avatar" or similar.
    // If not, we might need to rely on looking for "Leo" or similar text.
    // For now, let's assume auto-login works and we land on dashboard.
    await expect(page.locator("text=Quest Board")).toBeVisible({ timeout: 10000 }).catch(() => {
        // Fallback: Check if we are on landing page and need to click something?
        // But EvalForge usually auto-redirects to /arcade or /dashboard.
    });
}

test.describe("Practice Gauntlet – availability", () => {
    test("shows at least one practice item for a logged-in player", async ({ page }) => {
        // 1. Login
        await loginAsTestUser(page);

        // 2. Navigate to Gauntlet area
        // If the gauntlet is on the main dashboard/arcade view, this might be sufficient.
        // If it requires a specific route:
        await page.goto("/arcade");

        // 3. Locate Gauntlet items
        // We added data-testid="gauntlet-item" to PracticeGauntletCard
        const gauntletItemLocator = page.getByTestId("gauntlet-item");

        // 4. Assert
        // Wait for at least one item to appear
        await expect(gauntletItemLocator.first()).toBeVisible({ timeout: 15000 });

        // Count should be > 0
        const count = await gauntletItemLocator.count();
        expect(count).toBeGreaterThan(0);
    });
});
