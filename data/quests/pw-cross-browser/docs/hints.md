# Hints

## Hint 1
Add `test.use({ browserName: 'chromium' })` at the file level, before any test() calls.

## Hint 2
Fix the title assertion: use `/CMS Login/i` not `/WRONG/`.

## Hint 3
To assert the browser: `expect(page.context().browser()?.browserType().name()).toBe('chromium');`
