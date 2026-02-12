// TS Objects
// Normalize a partial configuration object into a complete config with defaults.

export type Config = {
    retries: number;
    timeoutMs: number;
    baseUrl: string;
    headers: Record<string, string>;
};

export function normalizeConfig(input: unknown): Config {
    const defaults = {
        retries: 3,
        timeoutMs: 500,
        baseUrl: "https://api.local",
        headers: { "x-client": "evalforge" },
    };

    if (!input || typeof input !== "object") {
        return defaults;
    }

    const inp = input as any;

    let retries = defaults.retries;
    if (typeof inp.retries === "number" && Number.isInteger(inp.retries)) {
        retries = Math.max(0, Math.min(10, inp.retries));
    }

    let timeoutMs = defaults.timeoutMs;
    if (typeof inp.timeoutMs === "number" && Number.isInteger(inp.timeoutMs)) {
        timeoutMs = Math.max(50, Math.min(5000, inp.timeoutMs));
    }

    let baseUrl = defaults.baseUrl;
    if (typeof inp.baseUrl === "string") {
        const trimmed = inp.baseUrl.trim();
        if (trimmed.length > 0) baseUrl = trimmed;
    }

    let headers = { ...defaults.headers };
    if (inp.headers && typeof inp.headers === "object" && !Array.isArray(inp.headers)) {
        // Merge input headers logic:
        // Test says: keys lowercased, values trimmed, drop empty keys/values.
        // It seems to replace defaults? Or merge?
        // Test `EF_TS_OBJECTS_HEADERS` output ONLY has `x-client` and `x-token`.
        // Input had `X-CLIENT` which overrode default.
        // Input had `X-Token`.
        // So we start with defaults, but if input has same key (case-insensitive), we overwrite?
        // Actually, easiest way is to process input headers into a normalized map, 
        // then merge onto defaults? Or merge first?

        // Wait, "headers: accept a plain object... trim values... lowercase keys... drop entries".

        // Let's look at `EF_TS_OBJECTS_HEADERS`:
        // Input: X-Token: " abc ", "": "nope", X-Empty: " ", X-CLIENT: "override"
        // Output: x-client: "override", x-token: "abc"

        // This implies we take the defaults, and overlay the normalized input headers.
        // Since `x-client` is in default, and input has `X-CLIENT`, the input one wins (normalized to `x-client`).

        const normInput: Record<string, string> = {};
        for (const [k, v] of Object.entries(inp.headers)) {
            if (typeof v !== "string") continue;
            const key = k.toLowerCase().trim();
            const val = v.trim();
            if (key.length > 0 && val.length > 0) {
                normInput[key] = val;
            }
        }

        headers = { ...defaults.headers, ...normInput };
    }

    return {
        retries,
        timeoutMs,
        baseUrl,
        headers,
    };
}
