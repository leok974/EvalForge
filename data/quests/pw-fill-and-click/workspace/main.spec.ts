import { test, expect } from '@playwright/test';

test('fill the login form and submit', async ({ page }) => {
  await page.goto('/login');

  // TODO: Fill the username field (data-testid="login-username") with 'admin'
  // TODO: Fill the password field (data-testid="login-password") with 'secret123'
  // TODO: Click the submit button (data-testid="login-submit")
  // TODO: Assert the URL contains '/dashboard' after login

  // Placeholder (replace this - expects dashboard but we never logged in):
  await expect(page).toHaveURL(/dashboard/);
});
