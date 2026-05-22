import { test, expect } from '@playwright/test';

// Explicitly configure the browser for this test file
test.use({ browserName: 'chromium' });

test('login page loads in chromium', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/CMS Login/i);
  // Assert the browser name reported by Playwright
  expect(page.context().browser()?.browserType().name()).toBe('chromium');
});
