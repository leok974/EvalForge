// TS Objects
// Normalize a partial/unknown config input into a full config with defaults.

export type Config = {
    retries: number;
    timeoutMs: number;
    baseUrl: string;
    headers: Record<string, string>;
};

const DEFAULTS: Config = {
    retries: 3,
    timeoutMs: 500,
    baseUrl: "https://api.local",
    headers: { "x-client": "evalforge" },
};

function isPlainObject(value: unknown): value is Record<string, unknown> {
    if (!value || typeof value !== "object") return false;
    const proto = Object.getPrototypeOf(value);
    return proto === Object.prototype || proto === null;
}

function clampInt(n: number, min: number, max: number): number {
    return Math.min(max, Math.max(min, n));
}

export function normalizeConfig(input: unknown): Config {
    // TODO: implement rules from README
    // Start from DEFAULTS, then overlay validated fields.
    return DEFAULTS;
}
