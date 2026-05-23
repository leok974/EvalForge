import { test, expect } from '@playwright/test';

test('cms title check', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/CMS Login/i);
});
