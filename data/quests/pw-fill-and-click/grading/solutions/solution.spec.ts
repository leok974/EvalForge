import { test, expect } from '@playwright/test';

test('fill the login form and submit', async ({ page }) => {
  await page.goto('/login');

  // Fill credentials
  await page.getByTestId('login-username').fill('admin');
  await page.getByTestId('login-password').fill('secret123');

  // Click submit
  await page.getByTestId('login-submit').click();

  // Assert redirect to dashboard
  await expect(page).toHaveURL(/dashboard/);
});
