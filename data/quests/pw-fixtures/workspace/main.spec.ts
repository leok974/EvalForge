import { test as base, expect } from '@playwright/test';

// TODO: Define a custom fixture called 'loggedInPage' that:
//   1. Navigates to /login
//   2. Fills credentials (admin / secret123)
//   3. Clicks submit
//   4. Yields the page (already on /dashboard)

// Placeholder - no fixture defined:
const test = base;

test('dashboard is accessible', async ({ page }) => {
  // TODO: use loggedInPage fixture instead of page
  // For now this will fail because we're not logged in:
  await expect(page.getByTestId('dashboard-title')).toBeVisible();
});
