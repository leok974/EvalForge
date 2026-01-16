import { test, expect } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'http://localhost:5174';

test('starter quest shows instructions when started from tutorial', async ({ page }) => {
    // 1. Navigate to root (redirects to /arcade/workshop)
    await page.goto(`${BASE_URL}/arcade/workshop`);

    // Wait for potential loading state
    await expect(page.locator('text=INITIALIZING LINK')).not.toBeVisible({ timeout: 15000 });

    // 2. Login (Initialize Session) if needed
    // Check if we are already logged in (user avatar or no login button)
    const loginBtn = page.locator('button', { hasText: 'Initialize Session' });
    if (await loginBtn.isVisible({ timeout: 5000 }).catch(() => false)) {
        await loginBtn.click();
    }

    // Wait for DevUI to load (user-avatar or similar indicator)
    // or wait for the "Welcome to EvalForge" tutorial dialog which appears for new users
    // We force tutorial in DevUI if local storage not set.
    // Ideally, use a fresh context or clear storage.

    // 3. Tutorial Dialog
    const tutorialDialog = page.locator('text=Welcome to EvalForge');
    await expect(tutorialDialog).toBeVisible({ timeout: 10000 });

    // 4. Click "Start your first quest"
    await page.locator('button:has-text("Start your first quest")').click();

    // 5. Verify Redirect and Active Quest Header
    // Should navigate to quest page
    // url should contain 'py-ignition-q1-warmup-script'
    await expect(page).toHaveURL(/.*py-ignition-q1-warmup-script.*/);

    // 6. Verify Active Quest Header in Terminal View
    // Header text: "Active Quest" (Visual label)
    await expect(page.locator('text=Active Quest').first()).toBeVisible();

    // Quest Title
    await expect(page.locator('text=Warmup Script – First Sparks')).toBeVisible();

    // Description
    await expect(page.locator('text=Write a tiny CLI script that greets the user and loops a few times.')).toBeVisible();
});
