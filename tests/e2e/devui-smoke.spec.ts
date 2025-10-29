import { test, expect, APIRequestContext } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'http://127.0.0.1:19010';

async function createSession(request: APIRequestContext, base: string = BASE_URL) {
  const resp = await request.post(`${base}/apps/arcade_app/users/test/sessions`);
  expect(resp.ok()).toBeTruthy();
  const json = await resp.json();
  expect(json.id).toBeTruthy();
  return json.id as string;
}

async function postMsg(request: APIRequestContext, base: string, sid: string, message: string) {
  const resp = await request.post(`${base}/apps/arcade_app/users/test/sessions/${sid}/query`, {
    data: { message }
  });
  expect(resp.ok()).toBeTruthy();
  return await resp.json();
}

test.describe('Dev UI + API smoke', () => {
  test('Dev UI at root and docs reachable', async ({ page, request }) => {
    // Root should serve the Dev UI
    await page.goto(`${BASE_URL}/`);
    await expect(page.locator('text=/EvalForge Dev UI/i')).toBeVisible({ timeout: 10000 });

    // Docs still reachable
    const docs = await request.get(`${BASE_URL}/docs`);
    expect(docs.ok()).toBeTruthy();
    const docsHtml = await docs.text();
    expect(docsHtml).toContain('swagger-ui');
  });

  test('API status moved to /api/status', async ({ request }) => {
    const res = await request.get(`${BASE_URL}/api/status`);
    expect(res.ok()).toBeTruthy();
    const json = await res.json();
    expect(json.status).toMatch(/running/i);
    expect(json.version).toMatch(/Phase 3/i);
  });

  test('Phase 3 minimal flow (greet -> track -> grade -> dedupe)', async ({ request }) => {
    const sid = await createSession(request);

    // 1) greet
    const r1 = await postMsg(request, BASE_URL, sid, 'hi');
    expect(r1.response).toBeTruthy();

    // 2) track select
    const r2 = await postMsg(request, BASE_URL, sid, '1');
    expect(r2.track ?? r2.state?.track).toBe('debugging');

    // 3) first grade
    const code = 'def add(a, b): return a + b';
    const r3 = await postMsg(request, BASE_URL, sid, code);
    // Should include last_grade; allow either top-level or nested under state
    const lg = r3.last_grade || r3.state?.last_grade;
    expect(lg).toBeTruthy();
    expect(lg.coverage).toBeDefined();
    expect(lg.correctness).toBeDefined();
    expect(lg.clarity).toBeDefined();
    const firstSha1 = r3.sha1;
    expect(firstSha1).toBeTruthy();

    // 4) dedupe on same code - should return same sha1 and indicate dedupe
    const r4 = await postMsg(request, BASE_URL, sid, code);
    expect(String(r4.response).toLowerCase()).toContain('already graded');
    expect(r4.sha1).toBe(firstSha1);
    const lg4 = r4.last_grade || r4.state?.last_grade;
    expect(lg4).toEqual(lg);
  });

  test('Hash normalization: near-duplicate (spaces/newlines) dedupes', async ({ request }) => {
    const sid = await createSession(request);

    // Setup: greet and select track
    await postMsg(request, BASE_URL, sid, 'hi');
    await postMsg(request, BASE_URL, sid, '1');

    // First submission with trailing newline
    const codeA = 'function add(a,b){return a+b}\n';
    const r1 = await postMsg(request, BASE_URL, sid, codeA);
    const firstSha1 = r1.sha1;
    expect(firstSha1).toBeTruthy();

    // Second submission with extra spaces and newlines (should normalize to same hash)
    const codeB = 'function add(a,b){return a+b}   \n\n';
    const r2 = await postMsg(request, BASE_URL, sid, codeB);
    
    // Should dedupe - same SHA1
    expect(r2.sha1).toBe(firstSha1);
    expect(String(r2.response).toLowerCase()).toContain('already graded');
    
    // Should reuse same grade
    const lg1 = r1.last_grade || r1.state?.last_grade;
    const lg2 = r2.last_grade || r2.state?.last_grade;
    expect(lg2).toEqual(lg1);
  });
});
