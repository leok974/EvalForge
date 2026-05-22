# Tutorial: API Testing with the request Fixture

## The request Fixture

Playwright's built-in `request` fixture creates an `APIRequestContext` that shares `baseURL` and cookies with the browser, but makes HTTP calls directly:

```typescript
test('api test', async ({ request }) => {
  const response = await request.get('/api/users');
  expect(response.status()).toBe(200);
  
  const data = await response.json();
  expect(data).toHaveLength(3);
});
```

## HTTP Methods

```typescript
// GET
const r = await request.get('/healthz');

// POST with JSON body
const r2 = await request.post('/api/login', {
  data: { username: 'admin', password: 'secret123' }
});

// POST with form data
const r3 = await request.post('/login', {
  form: { username: 'admin', password: 'secret123' }
});
```

## Asserting Responses

```typescript
expect(response.status()).toBe(200);
expect(response.ok()).toBeTruthy();  // status 200-299

const json = await response.json();
expect(json.status).toBe('ok');

const text = await response.text();
expect(text).toContain('hello');
```

## Mixing API and Browser

You can use both `request` and `page` in the same test:

```typescript
test('create via API, verify in browser', async ({ page, request }) => {
  await request.post('/api/items', { data: { name: 'test' } });
  await page.goto('/items');
  await expect(page.getByText('test')).toBeVisible();
});
```
