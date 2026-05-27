# Hints

## Hint 1
Call `page.route('**/search**', handler)` BEFORE navigating. Routes must be registered before the page makes the request.

## Hint 2
In the handler, use `route.fulfill({ status: 200, contentType: 'text/html', body: '...' })` to return custom HTML.

## Hint 3
```typescript
await page.route('**/search**', async route => {
  await route.fulfill({
    status: 200,
    contentType: 'text/html',
    body: '<html><body><p>INTERCEPTED</p></body></html>',
  });
});
await page.goto('/search?q=test');
await expect(page.getByText('INTERCEPTED')).toBeVisible();
```
