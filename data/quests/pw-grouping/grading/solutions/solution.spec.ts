import { test, expect } from '@playwright/test';

test.describe('CMS Dashboard Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Log in before each test
    await page.goto('/login');
    await page.getByTestId('login-username').fill('admin');
    await page.getByTestId('login-password').fill('secret123');
    await page.getByTestId('login-submit').click();
    await expect(page).toHaveURL(/dashboard/);
  });

  test('dashboard title is visible', async ({ page }) => {
    await expect(page.getByTestId('dashboard-title')).toBeVisible();
  });

  test('navigation links are visible', async ({ page }) => {
    await expect(page.getByRole('link', { name: 'Search Records' })).toBeVisible();
  });
});
