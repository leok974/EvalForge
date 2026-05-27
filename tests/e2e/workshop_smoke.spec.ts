import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:5173';

test.describe('Workshop Smoke Tests', () => {

    test('workshop loads and renders the workshop layout', async ({ page }) => {
        // /arcade/workshop routes through DevUI → WorkshopLayout.
        // WorkshopLayout always renders data-testid="layout-workshop".
        // (QuestBoard inside it only renders when a world context is set.)
        await page.goto(`${BASE_URL}/arcade/workshop`);
        await page.waitForLoadState('networkidle');

        const layout = page.getByTestId('layout-workshop');
        await expect(layout).toBeVisible({ timeout: 10000 });
    });

    test('active python quest has monaco editor and run button', async ({ page }) => {
        // Canonical URL: /arcade/worlds/{world_id}/quests/{slug}
        // (old /arcade/workshop/quests/ pattern was removed in the world-based routing refactor)
        const slug = 'python-systems-service-boundaries';
        const worldId = 'world-python';
        await page.goto(`${BASE_URL}/arcade/worlds/${worldId}/quests/${slug}`);
        await page.waitForLoadState('networkidle');

        // Monaco editor should be visible (confirms quest IDE loaded)
        const editor = page.locator('.monaco-editor').first();
        await expect(editor).toBeVisible({ timeout: 15000 });

        // Run button must be present
        const runBtn = page.locator('button:has-text("Run")').first();
        await expect(runBtn).toBeVisible();
    });

    // 'example execution produces output panel' DELETED Sprint 15:
    // Test body was empty (no assertions). The underlying execution coverage is
    // already provided by test_foundry_quest.spec.ts (full run-and-verify flow).
    // A world-entry dialog overlay (apps/web/src/components/ui/dialog.tsx) would
    // need a dismiss step before clicking Run; write a full test when that pattern
    // is established in the suite.

    // 'selenium quest shows preview tab' DELETED Sprint 15:
    // Quest slug 'python-selenium-basic-selectors' was retired and is not in the
    // database. Test body was empty. Re-add against an active selenium quest slug
    // when one with a Preview tab is seeded.

});
