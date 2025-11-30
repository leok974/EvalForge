/**
 * DevDiag Client Utility
 * 
 * Thin frontend client for EvalForge's DevDiag HTTP proxy.
 * Calls the backend proxy at /api/ops/diag which handles JWT authentication server-side.
 * 
 * Security:
 * - NO JWT tokens in frontend code
 * - Backend proxy handles all authentication
 * - Only passes diagnostic parameters (URL, preset)
 */

export interface DevDiagRequest {
  url: string;
  preset?: "chat" | "embed" | "app" | "full";
  tenant?: string;
}

export interface DevDiagResult {
  ok: boolean;
  result?: unknown;
  error?: string;
  playwright_report_url?: string;  // Optional URL to Playwright HTML report
  export_tar_url?: string;         // Optional URL to export archive
}

export interface DevDiagHealth {
  ok: boolean;
  message?: string;
}

/**
 * Run DevDiag diagnostics on a target URL via the backend proxy.
 * 
 * @param url - Target URL to diagnose
 * @param preset - Diagnostic preset (default: "app")
 * @param tenant - Tenant identifier (default: "evalforge")
 * @returns DevDiag result object
 * @throws Error if request fails or backend returns error
 * 
 * @example
 * ```ts
 * try {
 *   const result = await runDevDiag("https://evalforge.app");
 *   if (result.ok) {
 *     console.log("Diagnostics passed:", result.result);
 *   } else {
 *     console.error("Diagnostics failed:", result.error);
 *   }
 * } catch (error) {
 *   console.error("Request failed:", error);
 * }
 * ```
 */
export async function runDevDiag(
  url: string,
  preset: "chat" | "embed" | "app" | "full" = "app",
  tenant = "evalforge"
): Promise<DevDiagResult> {
  // Build request payload
  const request: DevDiagRequest = {
    url,
    preset,
    tenant,
  };

  // Call backend proxy at /api/ops/diag
  const response = await fetch("/api/ops/diag", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  // Handle HTTP errors (4xx, 5xx)
  if (!response.ok) {
    let errorMessage: string;
    
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorData.message || `HTTP ${response.status}`;
    } catch {
      errorMessage = `HTTP ${response.status}: ${response.statusText}`;
    }

    // Special handling for common error codes
    if (response.status === 503) {
      throw new Error("DevDiag server is not configured. Please set DEVDIAG_BASE in the server environment.");
    } else if (response.status === 504) {
      throw new Error("DevDiag diagnostic timed out. Please try again or use a simpler preset.");
    } else if (response.status === 429) {
      throw new Error("Rate limit exceeded. Please wait a moment before trying again.");
    }

    throw new Error(`DevDiag request failed: ${errorMessage}`);
  }

  // Parse and return result
  const result = await response.json() as DevDiagResult;
  return result;
}

/**
 * Check if DevDiag server is reachable via the backend proxy.
 * 
 * @returns Health check result
 * @throws Error if health check request fails
 * 
 * @example
 * ```ts
 * const health = await checkDevDiagHealth();
 * if (health.ok) {
 *   console.log("DevDiag is healthy");
 * } else {
 *   console.warn("DevDiag is unavailable:", health.message);
 * }
 * ```
 */
export async function checkDevDiagHealth(): Promise<DevDiagHealth> {
  const response = await fetch("/api/ops/diag/health", {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error(`Health check failed: HTTP ${response.status}`);
  }

  const health = await response.json() as DevDiagHealth;
  return health;
}

/**
 * Run DevDiag with automatic error handling and user-friendly messages.
 * 
 * Wraps runDevDiag() with error handling that returns a standardized result.
 * Useful for UI components that want graceful degradation.
 * 
 * @param url - Target URL to diagnose
 * @param preset - Diagnostic preset (default: "app")
 * @returns DevDiag result with ok=false on errors
 * 
 * @example
 * ```ts
 * const result = await safeRunDevDiag("https://evalforge.app");
 * // Always returns a result object, never throws
 * ```
 */
export async function safeRunDevDiag(
  url: string,
  preset: "chat" | "embed" | "app" | "full" = "app"
): Promise<DevDiagResult> {
  try {
    return await runDevDiag(url, preset);
  } catch (error) {
    return {
      ok: false,
      error: error instanceof Error ? error.message : String(error),
    };
  }
}
