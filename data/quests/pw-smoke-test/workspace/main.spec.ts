import { test, expect } from '@playwright/test';

test('cms title check', async ({ page }) => {
  await page.goto('/');
  // TODO: fix the assertion below - the title should match
  await expect(page).toHaveTitle(/WRONG_TITLE/);
});
