# Tutorial: Custom Fixtures with test.extend

## What are Fixtures?

Fixtures are Playwright's dependency injection system. They set up resources (pages, databases, auth state) and inject them into tests. Built-in fixtures include `page`, `browser`, `context`. You can extend them with your own.

## test.extend()

```typescript
import { test as base, expect, Page } from '@playwright/test';

const test = base.extend<{ loggedInPage: Page }>({
  loggedInPage: async ({ page }, use) => {
    // Setup: navigate and log in
    await page.goto('/login');
    await page.getByTestId('login-username').fill('admin');
    await page.getByTestId('login-password').fill('secret123');
    await page.getByTestId('login-submit').click();
    
    // Yield the page to the test
    await use(page);
    
    // Teardown (after use) - optional cleanup here
  },
});
```

## Using the Fixture

```typescript
test('dashboard visible', async ({ loggedInPage }) => {
  await expect(loggedInPage.getByTestId('dashboard-title')).toBeVisible();
});
```

## Why Fixtures Over beforeEach?

- Fixtures are composable (one fixture can use another)
- Fixtures are lazy (only created when a test requests them)
- Fixtures enable parallel isolation (each test gets its own fixture instance by default)
- Fixtures are scoped: `"test"` (default), `"worker"`, or `"file"`
