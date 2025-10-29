import { test, expect, APIRequestContext } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'http://127.0.0.1:19000';

async function createSession(request: APIRequestContext) {
  const resp = await request.post(`${BASE_URL}/apps/arcade_app/users/test/sessions`);
  expect(resp.ok()).toBeTruthy();
  const json = await resp.json();
  expect(json.id).toBeTruthy();
  return json.id as string;
}

async function postMsg(request: APIRequestContext, sid: string, message: string) {
  const resp = await request.post(`${BASE_URL}/apps/arcade_app/users/test/sessions/${sid}/query`, {
    data: { message }
  });
  expect(resp.ok()).toBeTruthy();
  return await resp.json();
}

test.describe('Dev UI + API smoke', () => {
  test('page loads and docs are reachable', async ({ page, request }) => {
    const root = await page.goto(`${BASE_URL}/`);
    expect(root?.ok()).toBeTruthy();

    const docs = await request.get(`${BASE_URL}/docs`);
    expect(docs.ok()).toBeTruthy();
    const docsHtml = await docs.text();
    expect(docsHtml).toContain('swagger-ui'); // generic marker in docs page
  });

  test('Phase 3 minimal flow (greet -> track -> grade -> dedupe)', async ({ request }) => {
    const sid = await createSession(request);

    // 1) greet
    const r1 = await postMsg(request, sid, 'hi');
    expect(r1.response).toBeTruthy();

    // 2) track select
    const r2 = await postMsg(request, sid, '1');
    expect(r2.track ?? r2.state?.track).toBe('debugging');

    // 3) first grade
    const code = 'def add(a, b): return a + b';
    const r3 = await postMsg(request, sid, code);
    // Should include last_grade; allow either top-level or nested under state
    const lg = r3.last_grade || r3.state?.last_grade;
    expect(lg).toBeTruthy();
    expect(lg.coverage).toBeDefined();
    expect(lg.correctness).toBeDefined();
    expect(lg.clarity).toBeDefined();

    // 4) dedupe on same code
    const r4 = await postMsg(request, sid, code);
    expect(String(r4.response)).toContain('already graded');
  });
});
