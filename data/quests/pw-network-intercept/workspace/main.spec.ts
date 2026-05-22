import { test, expect } from '@playwright/test';

test('intercept and modify a network request', async ({ page }) => {
  // TODO: Use page.route() to intercept requests to '/search*'
  // Fulfill the request with a custom HTML response containing the text 'INTERCEPTED'
  // Then navigate to '/search?q=test' and assert the page contains 'INTERCEPTED'

  // Placeholder - no route set up:
  await page.goto('/search?q=test');
  await expect(page.getByText('INTERCEPTED')).toBeVisible();
});
