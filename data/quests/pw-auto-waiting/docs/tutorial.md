# Tutorial: Playwright Auto-Waiting

## What is Auto-Waiting?

Playwright automatically waits for elements to be in a stable, actionable state before performing actions. You rarely need explicit `sleep()` or `waitFor()` calls.

## Default Timeout

The default timeout for actions and assertions is 30 seconds (configurable via `playwright.config.ts`). Until that timeout expires, Playwright retries.

```typescript
// This will retry until the element is visible, up to 30s:
await expect(page.getByTestId('delayed-protocol-box')).toBeVisible();
```

## When You Do Need Explicit Waits

Sometimes you need precise control:

```typescript
// Wait for element to be visible with custom timeout:
await expect(locator).toBeVisible({ timeout: 5000 });

// Wait for a specific condition:
await page.waitForSelector('[data-testid="results"]');
await page.waitForURL(/dashboard/);
await page.waitForLoadState('networkidle');
```

## Anti-Pattern: Hard Sleeps

Avoid `page.waitForTimeout(ms)` — it makes tests slow and brittle:

```typescript
// BAD:
await page.waitForTimeout(3000);
await expect(locator).toBeVisible();

// GOOD:
await expect(locator).toBeVisible();  // Playwright handles the wait
```

## See in practice: pw-auto-waiting
