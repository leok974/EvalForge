// TS Vars
// Export a constant greeting and a typed config object with literal values.

export const greeting = "System Online" as const;

export type Config = {
    retryLimit: 3;
    timeoutMs: 250;
    env: "dev";
};

export const config: Config = {
    retryLimit: 3,
    timeoutMs: 250,
    env: "dev",
};
