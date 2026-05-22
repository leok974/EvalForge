import { test, expect } from '@playwright/test';

test.skip('starter quest shows instructions when started from tutorial', async ({ page }) => {
    // SKIP — Sprint 15: three independent blockers:
    // 1. Hardcoded BASE_URL defaults to port 5174; the dev stack runs at 5173.
    // 2. Looks for 'Welcome to EvalForge' tutorial dialog — this dialog does not
    //    appear for mock auth users (auto-logged in as 'leo', no first-run modal shown).
    // 3. Quest slug 'py-ignition-q1-warmup-script' does not exist in the database.
    //    The foundry uses slugs like 'hello-variable', not 'py-ignition-q1-warmup-script'.
    // To fix: update the slug to a real first-run quest slug, confirm the onboarding
    // dialog exists for mock users, and use the playwright.config baseURL (remove
    // the hardcoded 5174 override).
    const BASE_URL = process.env.BASE_URL || 'http://localhost:5173';
    await page.goto(`${BASE_URL}/arcade/workshop`);
    await expect(page.locator('text=Welcome to EvalForge')).toBeVisible({ timeout: 10000 });
});
