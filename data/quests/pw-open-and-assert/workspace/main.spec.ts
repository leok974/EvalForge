import { test, expect } from '@playwright/test';

test('open the CMS and check the title', async ({ page }) => {
  // TODO: navigate to the root URL using page.goto('/')
  // Then assert the page title matches 'CMS Login'
  await page.goto('/');
  await expect(page).toHaveTitle(/WRONG_TITLE/);
});
