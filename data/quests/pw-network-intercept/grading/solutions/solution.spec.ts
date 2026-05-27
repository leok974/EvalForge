import { test, expect } from '@playwright/test';

test('intercept and modify a network request', async ({ page }) => {
  // Intercept requests to /search and return custom content
  await page.route('**/search**', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'text/html',
      body: '<html><body><p>INTERCEPTED</p></body></html>',
    });
  });

  await page.goto('/search?q=test');
  await expect(page.getByText('INTERCEPTED')).toBeVisible();
});
