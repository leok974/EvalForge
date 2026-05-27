# Hints

## Hint 1
Use `test.beforeEach` with the login sequence. The disputes endpoints don't actually require authentication in this CMS — but the pattern matters.

## Hint 2
For the "dispute detail page loads" test: use `page.getByTestId('view-4712923').click()` to navigate. Then assert `page.getByTestId('dispute-title')` is visible.

## Hint 3
For the resolve flow: click the resolve button and use `await expect(page.getByTestId('resolve-status')).toBeVisible({ timeout: 5000 })` — the status div appears after 1 second.
