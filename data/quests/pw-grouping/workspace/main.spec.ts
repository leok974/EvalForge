import { test, expect } from '@playwright/test';

// TODO: Use test.describe to group your tests under 'CMS Dashboard Tests'
// TODO: Use test.beforeEach to log in before each test
// TODO: Write two test cases:
//   1. Assert the dashboard title is visible
//   2. Assert the navigation links are visible

test('dashboard title is visible', async ({ page }) => {
  // Missing beforeEach login - this will fail
  await expect(page.getByTestId('dashboard-title')).toBeVisible();
});
