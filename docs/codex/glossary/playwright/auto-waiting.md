# Playwright Auto-Waiting

## Overview

One of Playwright's most powerful features is **auto-waiting**: before performing any action or assertion, Playwright automatically waits for the target element to be ready. This eliminates most explicit `sleep()` calls and makes tests more reliable.

---

## How Auto-Waiting Works

When you call `locator.click()`, `locator.fill()`, `expect(locator).toBeVisible()`, or any other action, Playwright:

1. Finds the element matching the locator
2. Checks that it passes **actionability checks** (see below)
3. Retries until the element is ready OR the timeout expires
4. Performs the action

```typescript
// Playwright waits for the button to be visible, enabled, and stable
await page.getByRole('button', { name: 'Submit' }).click();

// Playwright waits up to 30s for this element to become visible
await expect(page.getByTestId('delayed-content')).toBeVisible();
```

---

## Actionability Checks

Playwright performs different checks depending on the action:

| Action | Checks |
|--------|--------|
| `click()` | visible, stable, enabled, not obscured |
| `fill()` | visible, enabled, editable |
| `check()` / `uncheck()` | visible, stable, enabled |
| `expect().toBeVisible()` | visible |
| `expect().toBeEnabled()` | enabled |

---

## Default Timeout

The default timeout is **30 seconds** for actions and assertions. Configure it globally or per-action:

```typescript
// In playwright.config.ts:
export default defineConfig({
  timeout: 30000,       // per-test timeout
  expect: {
    timeout: 5000,      // per-assertion timeout
  },
});

// Per-assertion override:
await expect(locator).toBeVisible({ timeout: 10000 });

// Per-action override:
await locator.click({ timeout: 5000 });
```

---

## Common Assertion Matchers

```typescript
// Visibility
await expect(locator).toBeVisible();
await expect(locator).not.toBeVisible();
await expect(locator).toBeHidden();

// Enabled state
await expect(locator).toBeEnabled();
await expect(locator).toBeDisabled();

// Text content
await expect(locator).toHaveText('Expected text');
await expect(locator).toContainText('partial');

// Value (inputs)
await expect(locator).toHaveValue('admin');

// Count
await expect(locator).toHaveCount(3);

// URL
await expect(page).toHaveURL(/dashboard/);
await expect(page).toHaveTitle(/CMS/i);
```

---

## waitForSelector vs expect()

`page.waitForSelector()` is an older API. Prefer `expect()` matchers for assertions:

```typescript
// Old approach (works but verbose):
await page.waitForSelector('[data-testid="result"]', { state: 'visible' });

// Modern approach (preferred):
await expect(page.getByTestId('result')).toBeVisible();
```

Use `page.waitForSelector` only when you need the element object (not just to assert visibility).

---

## Load State Waiting

For navigation and page loads:

```typescript
// Wait for network to be idle (good for SPAs)
await page.waitForLoadState('networkidle');

// Wait for DOM content loaded
await page.waitForLoadState('domcontentloaded');

// Wait for specific URL
await page.waitForURL(/dashboard/);
await expect(page).toHaveURL(/dashboard/);
```

---

## Anti-Patterns

```typescript
// BAD: Hard sleep — wastes time and is still fragile
await page.waitForTimeout(3000);
await expect(locator).toBeVisible();

// GOOD: Let Playwright wait automatically
await expect(locator).toBeVisible();

// BAD: Polling manually
while (!(await locator.isVisible())) {
  await page.waitForTimeout(100);
}

// GOOD: Use expect with appropriate timeout
await expect(locator).toBeVisible({ timeout: 10000 });
```

---

## See in practice: pw-auto-waiting
