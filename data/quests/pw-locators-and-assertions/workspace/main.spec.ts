import { test, expect } from '@playwright/test';

test('locate elements on the login page', async ({ page }) => {
  await page.goto('/login');

  // TODO: Use getByRole to find the 'heading' element named 'CMS Login'
  // TODO: Use page.getByTestId('login-username') to locate the username input and assert it is visible

  // Placeholder (wrong selector - this should fail):
  const heading = page.getByRole('heading', { name: 'WRONG_HEADING_TEXT' });
  await expect(heading).toBeVisible();
});
