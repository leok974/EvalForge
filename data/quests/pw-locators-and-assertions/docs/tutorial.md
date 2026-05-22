# Tutorial: Playwright Locators

## Semantic Locators

Playwright recommends locators that reflect user intent, not implementation details.

### getByRole

Targets elements by ARIA role:

```typescript
page.getByRole('heading', { name: 'CMS Login' })
page.getByRole('button', { name: 'Login' })
page.getByRole('textbox', { name: 'Username' })
```

### getByTestId

Targets elements by `data-testid` attribute — the most stable selector for automated tests:

```typescript
page.getByTestId('login-username')
page.getByTestId('login-submit')
```

### getByText

Finds elements containing the specified text:

```typescript
page.getByText('CMS Login')
```

### getByPlaceholder

Finds inputs by their placeholder text:

```typescript
page.getByPlaceholder('Enter your email')
```

## Visibility Assertion

```typescript
await expect(locator).toBeVisible();
await expect(locator).not.toBeVisible();
```

## See in practice: pw-locators-and-assertions
