# Tutorial: Boss Quest — Full Flow Automation

## What Makes This Different

This is not a targeted exercise — it's a production-style test suite. You will combine all patterns from the Systems track: page objects, fixtures, assertions, auto-waiting, and screenshots.

## Disputes Workflow

The CMS has a `/disputes` list page and `/disputes/:id` detail pages. The workflow:
1. Login to access the protected pages
2. Visit `/disputes` — see the results table
3. Click a "View" link — navigate to the detail page
4. Read dispute information
5. Click "Resolve" — triggers async state change (success message appears)

## Key Testids

- `results-table` — the disputes list table
- `results-row-4712923` — a specific dispute row
- `view-4712923` — the view link for dispute 4712923
- `dispute-title` — the detail page heading
- `dispute-detail-panel` — the info panel
- `dispute-resolve-btn` — the resolve button
- `resolve-status` — the success message (hidden initially)

## Pattern: Async State Changes

The resolve button triggers a 1-second JS timeout before the success message appears. Use auto-waiting:

```typescript
await page.getByTestId('dispute-resolve-btn').click();
await expect(page.getByTestId('resolve-status')).toBeVisible({ timeout: 5000 });
```

## Screenshot Evidence

Always capture evidence at key points:

```typescript
await page.screenshot({ path: '/tmp/dispute-resolved.png' });
```
