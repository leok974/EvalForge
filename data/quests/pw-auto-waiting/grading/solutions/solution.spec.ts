import { test, expect } from '@playwright/test';

test('wait for delayed content to appear', async ({ page }) => {
  await page.goto('/latency?delay=1');

  // Playwright auto-waits up to the default timeout (30s in config).
  // The element appears after 1 second — no explicit wait needed.
  const box = page.getByTestId('delayed-protocol-box');
  await expect(box).toBeVisible();
});
