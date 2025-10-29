/**
 * API helpers for EvalForge Dev UI
 */
import { APIRequestContext } from '@playwright/test';

export async function createSession(request: APIRequestContext, base: string): Promise<string> {
  const r = await request.post(`${base}/apps/arcade_app/users/test/sessions`, {
    headers: { "Content-Length": "0" }
  });
  const j = await r.json();
  return j.id as string;
}

export async function send(request: APIRequestContext, base: string, sid: string, message: string) {
  const r = await request.post(`${base}/apps/arcade_app/users/test/sessions/${sid}/query`, {
    data: { message }
  });
  return await r.json();
}

// Lightweight browser/runtime helper (non-Playwright)
export async function getSessionStateFields(baseUrl: string | undefined, sid: string, fields: string[]): Promise<any> {
  const origin = baseUrl || (typeof window !== "undefined" ? window.location.origin : "http://127.0.0.1:19010");
  const qs = encodeURIComponent(fields.join(","));
  const res = await fetch(`${origin}/api/dev/session-state/${sid}?fields=${qs}`, {
    method: "GET",
    headers: { "Accept": "application/json" },
  });
  if (!res.ok) {
    throw new Error(`Session state fetch failed: ${res.status}`);
  }
  return res.json();
}
