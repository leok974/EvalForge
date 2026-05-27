import { test, expect } from '@playwright/test';

test('wait for delayed content to appear', async ({ page }) => {
  await page.goto('/latency?delay=1');

  // TODO: The element [data-testid="delayed-protocol-box"] appears after a 1 second delay.
  // Assert that it becomes visible. Playwright will auto-wait up to the default timeout.
  // Use: await expect(page.getByTestId('delayed-protocol-box')).toBeVisible();

  // Placeholder - this won't wait long enough:
  const box = page.getByTestId('delayed-protocol-box');
  await expect(box).toBeVisible({ timeout: 100 }); // too short!
});
