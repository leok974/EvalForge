import { test, expect, Page } from '@playwright/test';

async function login(page: Page) {
  await page.goto('/login');
  await page.getByTestId('login-username').fill('admin');
  await page.getByTestId('login-password').fill('secret123');
  await page.getByTestId('login-submit').click();
  await expect(page).toHaveURL(/dashboard/);
}

test.describe('Dispute Resolution Flow', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('disputes list is visible', async ({ page }) => {
    await page.goto('/disputes');
    const table = page.getByTestId('results-table');
    await expect(table).toBeVisible();
    await expect(page.getByTestId('results-row-4712923')).toBeVisible();
  });

  test('dispute detail page loads', async ({ page }) => {
    await page.goto('/disputes');
    await page.getByTestId('view-4712923').click();
    await expect(page).toHaveURL(/disputes\/4712923/);
    await expect(page.getByTestId('dispute-title')).toBeVisible();
    await expect(page.getByTestId('dispute-detail-panel')).toBeVisible();
  });

  test('resolve button is present', async ({ page }) => {
    await page.goto('/disputes/4712923');
    const resolveBtn = page.getByTestId('dispute-resolve-btn');
    await expect(resolveBtn).toBeVisible();
  });

  test('resolving dispute shows success', async ({ page }) => {
    await page.goto('/disputes/4712923');
    const resolveBtn = page.getByTestId('dispute-resolve-btn');
    await resolveBtn.click();

    // The resolve-status div appears after 1 second
    const status = page.getByTestId('resolve-status');
    await expect(status).toBeVisible({ timeout: 5000 });

    // Take a screenshot as evidence
    await page.screenshot({ path: '/tmp/dispute-resolved.png' });
  });
});
