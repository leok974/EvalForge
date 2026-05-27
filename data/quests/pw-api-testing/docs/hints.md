# Hints

## Hint 1
Use the `request` fixture (not `page`). The function signature is: `async ({ request }) => { ... }`.

## Hint 2
`request.get('/healthz')` makes a GET request using the configured `baseURL`.

## Hint 3
```typescript
const response = await request.get('/healthz');
expect(response.status()).toBe(200);
const body = await response.json();
expect(body.status).toBe('ok');
```
