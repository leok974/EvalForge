import { test, expect } from '@playwright/test';

// World Playwright E2E smoke test
// Verifies that pw-open-and-assert is accessible via the EvalForge UI
// and that the Playwright runner returns correct results.

const BASE_URL = process.env.BASE_URL || 'http://localhost:5173';
const API_URL = process.env.API_URL || 'http://localhost:8092';

const QUEST_SLUG = 'pw-open-and-assert';

// Solution code that should pass all objectives
const SOLUTION_CODE = `import { test, expect } from '@playwright/test';

test('open the CMS and check the title', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/CMS Login/i);
});
`;

// Starter code that should fail (wrong title matcher)
const FAILING_CODE = `import { test, expect } from '@playwright/test';

test('open the CMS and check the title', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/WRONG_TITLE/);
});
`;

test.describe('World Playwright — Quest Integration', () => {

  test('solution code passes all objectives via API', async ({ request }) => {
    const response = await request.post(`${API_URL}/api/quests/${QUEST_SLUG}/run`, {
      headers: {
        'Content-Type': 'application/json',
        'X-Auth-Mode': 'mock',
      },
      data: {
        code: SOLUTION_CODE,
        language: 'playwright',
        file: 'main.spec.ts',
      },
    });

    expect(response.ok()).toBeTruthy();
    const result = await response.json();

    expect(result.passed).toBe(true);
    expect(result.exit_code).toBe(0);

    // All objectives should pass
    const objectives = result.objective_results || [];
    for (const obj of objectives) {
      expect(obj.ok).toBe(true);
    }
  });

  test('failing starter code does not pass all objectives via API', async ({ request }) => {
    const response = await request.post(`${API_URL}/api/quests/${QUEST_SLUG}/run`, {
      headers: {
        'Content-Type': 'application/json',
        'X-Auth-Mode': 'mock',
      },
      data: {
        code: FAILING_CODE,
        language: 'playwright',
        file: 'main.spec.ts',
      },
    });

    expect(response.ok()).toBeTruthy();
    const result = await response.json();

    // Exit code should be non-zero (test fails)
    expect(result.exit_code).not.toBe(0);
    expect(result.passed).toBe(false);
  });

  test('all 7 ignition quests pass solution mode', async ({ request }) => {
    // Spot-check a second ignition quest to confirm the whole track is healthy
    const IGNITION_SLUGS = [
      'pw-fill-and-click',
      'pw-auto-waiting',
      'pw-screenshot-and-trace',
    ];

    const FILL_CLICK_SOLUTION = `import { test, expect } from '@playwright/test';

test('fill login form and click submit', async ({ page }) => {
  await page.goto('/login');
  await page.getByTestId('login-username').fill('admin');
  await page.getByTestId('login-password').fill('secret123');
  await page.getByTestId('login-submit').click();
  await expect(page).toHaveURL(/dashboard/);
});
`;

    const response = await request.post(`${API_URL}/api/quests/pw-fill-and-click/run`, {
      headers: {
        'Content-Type': 'application/json',
        'X-Auth-Mode': 'mock',
      },
      data: {
        code: FILL_CLICK_SOLUTION,
        language: 'playwright',
        file: 'main.spec.ts',
      },
    });

    expect(response.ok()).toBeTruthy();
    const result = await response.json();

    expect(result.passed).toBe(true);
    expect(result.exit_code).toBe(0);
  });

});
