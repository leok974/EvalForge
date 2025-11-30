/**
 * DevDiag Proxy E2E Tests
 * 
 * Smoke test for DevDiag HTTP proxy integration.
 * Tests health check and diagnostic endpoints with graceful degradation.
 */

import { test, expect } from "@playwright/test";

const BASE = process.env.BASE_URL || "http://127.0.0.1:19010";

test.describe("DevDiag Proxy", () => {
  test("@smoke health check works or degrades gracefully", async ({ request }) => {
    const response = await request.get(`${BASE}/api/ops/diag/health`);
    
    // Health check should always return 200, even if DevDiag server is unavailable
    expect(response.status()).toBe(200);
    
    const body = await response.json();
    expect(body).toHaveProperty("ok");
    expect(typeof body.ok).toBe("boolean");
    
    if (!body.ok) {
      // When DevDiag is unavailable, message should explain why
      expect(body).toHaveProperty("message");
      expect(body.message).toBeTruthy();
    }
  });

  test("@smoke diagnostic endpoint works or degrades gracefully", async ({ request }) => {
    const response = await request.post(`${BASE}/api/ops/diag`, {
      data: { 
        url: `${BASE}/healthz`, 
        preset: "app" 
      },
      headers: { 
        "Content-Type": "application/json" 
      },
    });

    // Accept either success (200) or graceful degrade (503)
    // Never 5xx other than 503
    expect([200, 503]).toContain(response.status());
    
    const body = await response.json();
    
    if (response.status() === 200) {
      // Success: DevDiag ran successfully
      expect(body.ok).toBe(true);
      expect(body).toHaveProperty("result");
      expect(body.result).toBeTruthy();
    } else if (response.status() === 503) {
      // Graceful degradation: DevDiag server not configured/available
      expect(body).toHaveProperty("detail");
      expect(body.detail).toContain("not configured");
    }
  });

  test("@smoke diagnostic endpoint validates request schema", async ({ request }) => {
    // Missing required 'url' field should return 422
    const response = await request.post(`${BASE}/api/ops/diag`, {
      data: { 
        preset: "app" 
        // Missing 'url' field
      },
      headers: { 
        "Content-Type": "application/json" 
      },
    });

    expect(response.status()).toBe(422);
    const body = await response.json();
    expect(body).toHaveProperty("detail");
  });

  test("@smoke diagnostic endpoint handles invalid JSON", async ({ request }) => {
    const response = await request.post(`${BASE}/api/ops/diag`, {
      data: "not valid json",
      headers: { 
        "Content-Type": "application/json" 
      },
      failOnStatusCode: false,
    });

    expect(response.status()).toBe(422);
  });

  test("diagnostic endpoint returns proper error for timeout", async ({ request }) => {
    // This test assumes DevDiag server is running but might be slow
    // Skip if DevDiag is not available
    const healthCheck = await request.get(`${BASE}/api/ops/diag/health`);
    const health = await healthCheck.json();
    
    if (!health.ok) {
      test.skip();
    }

    // Note: Actual timeout testing requires a slow endpoint
    // This is a placeholder that validates the endpoint structure
    const response = await request.post(`${BASE}/api/ops/diag`, {
      data: { 
        url: `${BASE}/healthz`, 
        preset: "app" 
      },
      headers: { 
        "Content-Type": "application/json" 
      },
      timeout: 5000, // Client timeout shorter than server timeout
    });

    // Should complete successfully or return proper error
    expect([200, 503, 504]).toContain(response.status());
  });
});
