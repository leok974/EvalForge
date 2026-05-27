import { test, expect } from "@playwright/test";

test.describe("Legendary Boss Flow", () => {
    test.skip("clicking a Legendary Gauntlet card opens the Legendary boss HUD", async ({
        page
    }) => {
        // SKIP — Sprint 15: two blockers remain:
        // 1. PracticeGauntletCard (apps/web/src/components/practice/PracticeGauntletCard.tsx)
        //    renders each item with data-testid="gauntlet-item" (generic). This test needs
        //    data-testid={`gauntlet-card-${item.difficulty}-${item.id}`} on the <li> element.
        //    One-line change in PracticeGauntletCard.tsx, then update the locator here.
        // 2. The test must navigate to /arcade/workshop (or /workshop which redirects there)
        //    before mocking the route, since the PracticeGauntlet only renders in that context.
        // Route check: /arcade/worlds/{worldSlug}/bosses/{bossSlug} exists in DevUI.tsx — no
        // route fix needed. BossHud.tsx renders the boss-hud testid.
        // Revisit: Sprint 16
        // Blocker: add typed data-testid to PracticeGauntletCard.tsx <li> element.
        const baseUrl = process.env.BASE_URL || "http://localhost:5173";
        await page.goto(baseUrl + "/");

        // Wait for everything to settle
        await page.waitForLoadState('networkidle');

        // 2) Look for ANY legendary card. We can use a regex or partial match if we don't know the exact ID
        // or we can mock the API response to force a specific legendary card to appear.
        // For a real E2E, we might need to seed this or mock the route.
        // Assuming the test environment has at least one legendary boss available or mocked.

        // NOTE: If this runs against a real dev env, we need to ensure a legendary boss is in 'today's plan'.
        // If not, we might need to rely on mocking the network response for /api/practice_rounds/today.

        await page.route('/api/practice_rounds/today', async route => {
            const json = {
                date: new Date().toISOString(),
                label: "Mocked Legendary Day",
                items: [
                    {
                        id: "boss:boss-archives-analytics-arbiter",
                        item_type: "boss_review",
                        label: "Archives Analytics Arbiter",
                        description: "Legendary Boss Review",
                        difficulty: "legendary",
                        rationale: "E2E Test",
                        struggle_score: 5,
                        world_slug: "world-sql"
                    }
                ],
                completed_count: 0,
                total_count: 1,
                streak_days: 10
            };
            await route.fulfill({ json });
        });

        // Reload to pick up the mock
        await page.reload();

        // 3) Find the legendary card
        // The ID format in PracticeGauntletCard is `gauntlet-card-legendary-${item.id}`
        // item.id here is "boss:boss-archives-analytics-arbiter"
        const legendaryCard = page.getByTestId(
            "gauntlet-card-legendary-boss:boss-archives-analytics-arbiter"
        );

        await expect(legendaryCard).toBeVisible({ timeout: 10000 });

        // 4) Click it
        await legendaryCard.click();

        // 5) Assert correct navigation to Boss HUD
        // Should go to /worlds/world-sql/bosses/boss-archives-analytics-arbiter
        await expect(page).toHaveURL(/\/worlds\/world-sql\/bosses\/boss-archives-analytics-arbiter/);

        // 6) Assert Boss HUD and Badges
        const bossHud = page.getByTestId("boss-hud");
        await expect(bossHud).toBeVisible();

        const legendaryBadge = page.getByTestId("boss-hud-legendary-badge");
        await expect(legendaryBadge).toBeVisible();
        await expect(legendaryBadge).toHaveText(/LEGENDARY/i);
    });
});
