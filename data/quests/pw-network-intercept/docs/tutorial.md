# Tutorial: Network Interception with page.route()

## page.route()

`page.route(pattern, handler)` intercepts matching requests before they leave the browser:

```typescript
// Intercept all requests to /api/users
await page.route('**/api/users', async route => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([{ id: 1, name: 'Mock User' }]),
  });
});
```

## Pattern Matching

Use glob patterns:
- `'**/search**'` — any URL containing "search"
- `'**/api/**'` — any URL with /api/ in the path
- `'https://example.com/data'` — exact URL

## route.fulfill()

Returns a custom response:

```typescript
await route.fulfill({
  status: 200,
  contentType: 'text/html',
  body: '<html><body>Custom Response</body></html>',
});
```

## route.continue()

Let the request through (useful for selective interception):

```typescript
await page.route('**/*', async route => {
  if (route.request().url().includes('ads')) {
    await route.abort();
  } else {
    await route.continue();
  }
});
```

## route.abort()

Blocks the request entirely, simulating network failure.
