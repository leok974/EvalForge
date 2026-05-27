import { test, expect } from '@playwright/test';
import * as fs from 'fs';

test('capture a screenshot of the login page', async ({ page }) => {
  await page.goto('/');

  const screenshotPath = '/tmp/cms-login.png';
  await page.screenshot({ path: screenshotPath });

  // Verify the file was written to disk
  expect(fs.existsSync(screenshotPath)).toBe(true);
});
