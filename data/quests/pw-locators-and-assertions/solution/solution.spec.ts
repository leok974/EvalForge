import { test, expect } from '@playwright/test';

test('locate elements on the login page', async ({ page }) => {
  await page.goto('/login');

  // Use getByRole to find the heading
  const heading = page.getByRole('heading', { name: 'CMS Login' });
  await expect(heading).toBeVisible();

  // Use getByTestId to locate the username input
  const usernameInput = page.getByTestId('login-username');
  await expect(usernameInput).toBeVisible();

  // Use getByRole to find the submit button
  const submitBtn = page.getByRole('button', { name: 'Login' });
  await expect(submitBtn).toBeVisible();
});
