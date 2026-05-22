import { test, expect } from '@playwright/test';

test('health check via API request', async ({ request }) => {
  // TODO: Use request.get() to call GET /healthz
  // Assert the response status is 200
  // Assert the JSON body contains { "status": "ok" }

  // Placeholder - wrong endpoint:
  const response = await request.get('/nonexistent');
  expect(response.status()).toBe(200);
});
