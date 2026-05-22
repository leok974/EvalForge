# Tutorial: fill() and click()

## Filling Inputs

`locator.fill(value)` clears an input and types the given value:

```typescript
await page.getByTestId('login-username').fill('admin');
await page.getByLabel('Password').fill('secret123');
```

## Clicking Elements

`locator.click()` clicks the element:

```typescript
await page.getByTestId('login-submit').click();
await page.getByRole('button', { name: 'Login' }).click();
```

## Asserting Navigation

After a form submission that redirects, assert the new URL:

```typescript
await expect(page).toHaveURL(/dashboard/);
await expect(page).toHaveURL('/dashboard');
```

Playwright auto-waits for navigation to complete before the assertion runs.

## Full Example

```typescript
await page.goto('/login');
await page.getByTestId('login-username').fill('admin');
await page.getByTestId('login-password').fill('secret123');
await page.getByTestId('login-submit').click();
await expect(page).toHaveURL(/dashboard/);
```
