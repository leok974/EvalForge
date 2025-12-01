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

export async function sendSessionMessage(baseUrl: string | undefined, sid: string, text: string) {
  const origin = baseUrl || (typeof window !== "undefined" ? window.location.origin : "http://127.0.0.1:19010");
  const res = await fetch(`${origin}/apps/arcade_app/users/test/sessions/${sid}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text }),
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`Query failed: ${res.status} ${body}`);
  }
  return res.json(); // { response: string }
}

export async function sendSessionMessageStream(
  baseUrl: string | undefined,
  sid: string,
  text: string,
  handlers: {
    onStart?: () => void;
    onDelta?: (token: string) => void;
    onFinal?: (fullText: string) => void;
    onDone?: () => void;
    onError?: (error: string) => void;
  },
  abortSignal?: AbortSignal,
  context?: { codex_id?: string; track_id?: string; world_id?: string }
) {
  const origin = baseUrl || (typeof window !== "undefined" ? window.location.origin : "http://127.0.0.1:19010");
  const res = await fetch(`${origin}/apps/arcade_app/users/test/sessions/${sid}/query/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "Accept": "text/event-stream" },
    body: JSON.stringify({
      message: text,
      ...context
    }),
    signal: abortSignal,
  });

  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`Stream failed: ${res.status} ${body}`);
  }

  const reader = res.body?.getReader();
  if (!reader) throw new Error("No response body");

  const decoder = new TextDecoder();
  let buffer = "";

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const data = line.slice(6);
        if (!data.trim()) continue;

        try {
          const evt = JSON.parse(data);
          if (evt.type === "start") handlers.onStart?.();
          else if (evt.type === "delta" && evt.text) handlers.onDelta?.(evt.text);
          else if (evt.type === "final" && evt.text !== undefined) handlers.onFinal?.(evt.text);
          else if (evt.type === "done") handlers.onDone?.();
          else if (evt.type === "error") handlers.onError?.(evt.message || "Unknown error");
        } catch (e) {
          console.error("SSE parse error:", e, data);
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

