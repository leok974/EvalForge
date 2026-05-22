import { test, expect } from '@playwright/test';

test('health check via API request', async ({ request }) => {
  const response = await request.get('/healthz');
  expect(response.status()).toBe(200);

  const body = await response.json();
  expect(body.status).toBe('ok');
});
