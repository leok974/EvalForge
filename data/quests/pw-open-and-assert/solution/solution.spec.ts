import { test, expect } from '@playwright/test';

test('open the CMS and check the title', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/CMS Login/i);
});
