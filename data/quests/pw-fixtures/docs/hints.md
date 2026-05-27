# Hints

## Hint 1
Use `const test = base.extend<{ loggedInPage: Page }>({ ... })` to create a custom test with the new fixture.

## Hint 2
Inside the fixture, perform login, then call `await use(page)` to yield the authenticated page to the test.

## Hint 3
```typescript
const test = base.extend<{ loggedInPage: Page }>({
  loggedInPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.getByTestId('login-username').fill('admin');
    await page.getByTestId('login-password').fill('secret123');
    await page.getByTestId('login-submit').click();
    await use(page);
  },
});
```
