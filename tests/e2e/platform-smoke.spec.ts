import { test, expect } from '@playwright/test';

// Ensure the app is running via 'npm run dev' or docker before running this
const BASE_URL = 'http://localhost:8092';

test.describe('EvalForge Platform Smoke Test', () => {

    test('Phase 1: Multi-Agent Routing', async ({ page }) => {
        await page.goto(BASE_URL);

        // 1. Select World (Assuming Python World is default or available)
        // We target the select via internal structure or values
        const worldSelect = page.locator('select').first();
        await worldSelect.selectOption({ label: '🐍 Python World' });

        // 2. Select Quest Mode
        await page.click('button:has-text("QUEST")');

        // 3. Send Message
        await page.fill('textarea', 'start');
        await page.click('button:has-text("RUN")');

        // 4. Verify Stream Response
        // We expect the "QuestMaster" persona to respond
        await expect(page.locator('text=Quest:')).toBeVisible({ timeout: 10000 });
    });

    test('Phase 2: Codex System', async ({ page }) => {
        await page.goto(BASE_URL);

        // 1. Open Codex
        await page.click('button:has-text("📖 CODEX")');

        // 2. Verify Drawer Opens
        await expect(page.locator('text=CODEX SYSTEM')).toBeVisible();

        // 3. Check for Index Entries
        // Assuming we have 'FastAPI Basics' from previous setup
        await expect(page.locator('text=FastAPI')).toBeVisible();

        // 4. Click Entry
        await page.click('text=FastAPI');

        // 5. Verify Markdown Content Rendered
        await expect(page.locator('h1:has-text("FastAPI Basics")')).toBeVisible();
    });
});
