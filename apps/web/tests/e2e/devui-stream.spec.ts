import { test, expect } from "@playwright/test";

const BASE = process.env.BASE_URL || "http://127.0.0.1:19010";

test("@smoke stream emits frames", async ({ request }) => {
  // Create session
  const s = await request.post(`${BASE}/apps/arcade_app/users/test/sessions`, { 
    data: "" 
  });
  expect(s.ok()).toBeTruthy();
  const sid = (await s.json()).id as string;

  // Kick off stream (raw fetch to get full response body)
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
  
  // We should see at least start and done frames, and ideally a final
  expect(body).toContain('data: {"type":"start"}');
  expect(body).toContain('"type":"final"');
  expect(body).toContain('data: {"type":"done"}');
});
