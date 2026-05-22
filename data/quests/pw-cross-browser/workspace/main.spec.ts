import { test, expect } from '@playwright/test';

// TODO: Use test.use({ browserName: 'chromium' }) to explicitly target chromium
// Then navigate to the login page and assert the title is visible

// Placeholder - missing test.use configuration:
test('login page loads in chromium', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/WRONG/);
});
