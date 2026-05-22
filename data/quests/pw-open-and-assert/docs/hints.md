# Hints

## Hint 1
`page.goto('/')` navigates using the `baseURL` configured in `playwright.config.ts`. You don't need the full URL.

## Hint 2
`expect(page).toHaveTitle(/CMS Login/i)` uses a regex with the `i` flag for case-insensitive matching. The actual title on the page is "CMS Login".

## Hint 3
Your solution should look like:
```typescript
await page.goto('/');
await expect(page).toHaveTitle(/CMS Login/i);
```
