# Playwright Debugging Guide

## Overview

When a Playwright test fails, you need fast insight into what the browser was doing. This guide covers the primary debugging tools: headed mode, `page.pause()`, the trace viewer, screenshot-on-failure, and verbose logging.

---

## 1. Run in Headed Mode

The most immediate debugging tool: make the browser visible.

```bash
# Run a specific test file in headed mode
npx playwright test my.spec.ts --headed

# Slow down interactions to watch what happens
npx playwright test my.spec.ts --headed --slow-mo=500
```

In headed mode you see exactly what the browser renders at each step.

---

## 2. page.pause()

`page.pause()` stops test execution and opens Playwright Inspector — an interactive debugger with a step-through interface:

```typescript
test('debug this test', async ({ page }) => {
  await page.goto('/login');
  await page.pause();  // Opens Inspector, test pauses here
  await page.getByTestId('login-username').fill('admin');
});
```

In the Inspector you can:
- Step through remaining actions
- Use the locator picker to find element selectors
- Execute Playwright commands in the console

**Note:** `page.pause()` only works in headed mode. Remove it before committing.

---

## 3. Trace Viewer

The trace viewer records a complete execution trace: screenshots, network requests, DOM snapshots at every step. It is the most powerful post-mortem tool.

### Enable in config

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    trace: 'on-first-retry',  // Record trace on first test failure
    // Options: 'off' | 'on' | 'retain-on-failure' | 'on-first-retry'
  },
});
```

### Record programmatically

```typescript
test('with trace', async ({ page, context }) => {
  await context.tracing.start({ screenshots: true, snapshots: true });
  await page.goto('/login');
  // ... test actions ...
  await context.tracing.stop({ path: '/tmp/trace.zip' });
});
```

### View the trace

```bash
npx playwright show-trace /tmp/trace.zip
```

This opens a browser-based viewer with a timeline of all actions, network calls, and console logs.

---

## 4. Screenshot on Failure

Capture screenshots automatically when tests fail:

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    screenshot: 'only-on-failure',  // 'off' | 'on' | 'only-on-failure'
    video: 'retain-on-failure',
  },
});
```

Or capture manually at any point:

```typescript
test('with manual screenshot', async ({ page }) => {
  await page.goto('/login');
  
  // Capture before an action you're debugging
  await page.screenshot({ path: '/tmp/before-login.png' });
  
  await page.getByTestId('login-username').fill('admin');
  
  // Capture the current state after the action
  await page.screenshot({ path: '/tmp/after-fill.png' });
});
```

---

## 5. Verbose Logging

Enable verbose output to see Playwright's internal logs:

```bash
# Show all Playwright API calls
DEBUG=pw:api npx playwright test my.spec.ts

# Show browser console logs
DEBUG=pw:browser npx playwright test my.spec.ts

# Show all debug output
DEBUG=pw:* npx playwright test my.spec.ts
```

### Capture browser console in tests

```typescript
page.on('console', msg => {
  console.log(`Browser [${msg.type()}]: ${msg.text()}`);
});

page.on('pageerror', err => {
  console.error(`Page error: ${err.message}`);
});
```

---

## 6. Common Failure Patterns

### "Element not found" / Timeout

The element doesn't exist or isn't visible yet:

```typescript
// Check: Is the selector correct?
// Use page.pause() and the Inspector to verify the locator
await page.pause();

// Check: Is there a timing issue?
// Increase timeout or check for race conditions
await expect(locator).toBeVisible({ timeout: 10000 });
```

### "Element is not actionable"

The element exists but isn't ready (e.g., disabled, covered by overlay):

```typescript
// Wait for the element to be enabled
await expect(locator).toBeEnabled();
await locator.click();
```

### Wrong URL after navigation

The navigation succeeded but the URL is different from expected:

```typescript
// Use regex for flexible matching
await expect(page).toHaveURL(/dashboard/);

// Or check the current URL
console.log('Current URL:', page.url());
```

---

## 7. Debugging Checklist

1. Run with `--headed` to see the browser
2. Add `await page.pause()` before the failing line
3. Check the selector with the Inspector's locator picker
4. Enable `screenshot: 'only-on-failure'` in config
5. Enable `trace: 'on-first-retry'` and run `show-trace` to review the full execution
6. Check browser console logs for JavaScript errors
