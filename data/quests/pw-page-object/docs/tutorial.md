# Tutorial: Page Object Model

## What is a Page Object?

A Page Object encapsulates a page's selectors and actions into a TypeScript class. Tests use the class methods, not raw Playwright calls, making tests readable and maintainable.

## Basic Structure

```typescript
import { Page } from '@playwright/test';

class LoginPage {
  constructor(private page: Page) {}

  async navigate() {
    await this.page.goto('/login');
  }

  async login(username: string, password: string) {
    await this.page.getByTestId('login-username').fill(username);
    await this.page.getByTestId('login-password').fill(password);
    await this.page.getByTestId('login-submit').click();
  }

  async getErrorMessage() {
    return this.page.getByTestId('login-error').textContent();
  }
}
```

## Using the Page Object in Tests

```typescript
test('successful login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.navigate();
  await loginPage.login('admin', 'secret123');
  await expect(page).toHaveURL(/dashboard/);
});

test('failed login shows error', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.navigate();
  await loginPage.login('wrong', 'credentials');
  const error = await loginPage.getErrorMessage();
  expect(error).toContain('Invalid');
});
```

## Benefits

- Locators defined once, used everywhere
- Refactoring a locator requires one change
- Tests read like natural language
