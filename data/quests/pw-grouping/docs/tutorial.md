# Tutorial: test.describe and beforeEach

## test.describe

Groups related tests together. The group name appears in reports:

```typescript
test.describe('User Login', () => {
  test('shows error on bad credentials', async ({ page }) => { ... });
  test('redirects to dashboard on success', async ({ page }) => { ... });
});
```

## test.beforeEach

Runs before every test in the current describe block or file:

```typescript
test.describe('Dashboard Tests', () => {
  test.beforeEach(async ({ page }) => {
    // This login runs before EACH test below
    await page.goto('/login');
    await page.getByTestId('login-username').fill('admin');
    await page.getByTestId('login-password').fill('secret123');
    await page.getByTestId('login-submit').click();
  });

  test('title is visible', async ({ page }) => {
    await expect(page.getByTestId('dashboard-title')).toBeVisible();
  });

  test('nav links present', async ({ page }) => {
    await expect(page.getByRole('link', { name: 'Search Records' })).toBeVisible();
  });
});
```

## test.afterEach / test.afterAll

Clean up after each test or once after all tests in the group.

## test.beforeAll

Runs once before all tests in the group (shared state — use with care in parallel runs).
