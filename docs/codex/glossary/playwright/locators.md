# Playwright Locators

## Overview

Locators are Playwright's core mechanism for finding elements on a page. Unlike traditional CSS selectors, Playwright locators are lazy — they only perform the actual element lookup when you perform an action or assertion, and they automatically retry until the element is in an actionable state.

Playwright strongly recommends **semantic locators** that reflect how users interact with the page, rather than implementation details like CSS class names.

---

## getByRole()

Finds elements by their ARIA role and optional accessible name. This is the most resilient locator strategy — roles reflect semantic HTML meaning and ARIA attributes.

```typescript
// Find a button by its accessible name
const submitBtn = page.getByRole('button', { name: 'Login' });

// Find a heading
const heading = page.getByRole('heading', { name: 'CMS Dashboard' });

// Find a text input (role: textbox)
const emailInput = page.getByRole('textbox', { name: 'Email' });

// Find a link
const navLink = page.getByRole('link', { name: 'Search Records' });
```

Common ARIA roles: `button`, `heading`, `textbox`, `link`, `checkbox`, `radio`, `combobox`, `table`, `row`, `cell`.

---

## getByTestId()

Finds elements by their `data-testid` attribute. This is the recommended approach for automation-specific targeting — test IDs don't change with styling or text updates.

```typescript
const usernameField = page.getByTestId('login-username');
const dashboardTitle = page.getByTestId('dashboard-title');
const resultsTable = page.getByTestId('results-table');
```

Configure the attribute name in `playwright.config.ts`:

```typescript
export default defineConfig({
  use: { testIdAttribute: 'data-testid' },  // default
});
```

---

## getByText()

Finds elements by their visible text content. Useful for asserting dynamic content.

```typescript
// Exact match
const item = page.getByText('Billing Dispute');

// Partial match (default)
const status = page.getByText('Active', { exact: false });

// Exact match with option
const exactMatch = page.getByText('CMS Login', { exact: true });
```

---

## getByLabel()

Finds form inputs associated with a `<label>` element.

```typescript
const passwordField = page.getByLabel('Password');
const searchBox = page.getByLabel('Search query');
```

---

## getByPlaceholder()

Finds inputs by their `placeholder` attribute text.

```typescript
const emailInput = page.getByPlaceholder('Enter your email');
const searchBox = page.getByPlaceholder('Search...');
```

---

## CSS and XPath Selectors

For cases where semantic locators aren't available:

```typescript
// CSS selector
const el = page.locator('[data-testid="my-element"]');
const classEl = page.locator('.my-class');

// XPath
const xpathEl = page.locator('//button[contains(text(), "Submit")]');
```

Prefer CSS over XPath — CSS selectors are faster and more readable.

---

## Chaining Locators

Narrow down a locator within a parent element:

```typescript
const row = page.getByTestId('results-row-4712923');
const viewLink = row.getByRole('link');
await viewLink.click();
```

---

## Locator vs ElementHandle

Playwright's `Locator` is the modern API. `ElementHandle` is the legacy approach. Always use `Locator`:

```typescript
// Modern (preferred):
await page.getByRole('button').click();

// Legacy (avoid):
const el = await page.$('button');
await el?.click();
```

---

## See in practice: pw-locators-and-assertions
