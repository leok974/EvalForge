import { test, expect } from "@playwright/test";

const BASE = process.env.BASE_URL || "http://127.0.0.1:19010";

test("@smoke session create -> first query works", async ({ request }) => {
  // Create session (local store only)
  const s = await request.post(`${BASE}/apps/arcade_app/users/test/sessions`, { 
    data: "" 
  });
  expect(s.ok()).toBeTruthy();
  const sid = (await s.json()).id as string;
  expect(sid).toBeTruthy();
  expect(typeof sid).toBe("string");

  // First query should lazy-create ADK session (no INVALID_ARGUMENT)
  const q = await request.post(
    `${BASE}/apps/arcade_app/users/test/sessions/${sid}/query`, 
    {
      data: { message: "hi" }
    }
  );
  
  expect(q.ok()).toBeTruthy();
  const body = await q.json();
  expect(typeof body.response).toBe("string");
  expect(body.session_id).toBe(sid);
});

test("@smoke session create -> streaming query works", async ({ request }) => {
  // Create session
  const s = await request.post(`${BASE}/apps/arcade_app/users/test/sessions`, { 
    data: "" 
  });
  expect(s.ok()).toBeTruthy();
  const sid = (await s.json()).id as string;

  // Stream a message (should create ADK session and stream response)
  const r = await request.fetch(
    `${BASE}/apps/arcade_app/users/test/sessions/${sid}/query/stream`, 
    {
      method: "POST",
      headers: { 
        "Content-Type": "application/json", 
        "Accept": "text/event-stream" 
      },
      data: { message: "hi" }
    }
  );
  
  expect(r.ok()).toBeTruthy();
  const body = await r.text();
  
  // Verify SSE frames are present
  expect(body).toContain('data: {"type":"start"}');
  expect(body).toContain('"type":"final"');
  expect(body).toContain('data: {"type":"done"}');
  
  // Should not contain error frames
  expect(body).not.toContain('"type":"error"');
  expect(body).not.toContain('INVALID_ARGUMENT');
});
