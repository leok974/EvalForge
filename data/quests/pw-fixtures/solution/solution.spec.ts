import { test as base, expect, Page } from '@playwright/test';

// Extend the base test with a loggedInPage fixture
const test = base.extend<{ loggedInPage: Page }>({
  loggedInPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.getByTestId('login-username').fill('admin');
    await page.getByTestId('login-password').fill('secret123');
    await page.getByTestId('login-submit').click();
    await expect(page).toHaveURL(/dashboard/);
    await use(page);
  },
});

test('dashboard is accessible', async ({ loggedInPage }) => {
  await expect(loggedInPage.getByTestId('dashboard-title')).toBeVisible();
});

test('search link is visible', async ({ loggedInPage }) => {
  await expect(loggedInPage.getByRole('link', { name: 'Search Records' })).toBeVisible();
});
