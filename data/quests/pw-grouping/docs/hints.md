# Hints

## Hint 1
Wrap all your tests in `test.describe('CMS Dashboard Tests', () => { ... })`.

## Hint 2
Inside the describe block, add `test.beforeEach(async ({ page }) => { ... })` with the full login sequence before any `test(...)` calls.

## Hint 3
Two test cases are needed. Use `page.getByTestId('dashboard-title')` for the title check and `page.getByRole('link', { name: 'Search Records' })` for the navigation check.
