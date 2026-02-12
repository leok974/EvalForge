function readPort() {
    const raw = process.env.PORT;
    if (raw == null || raw.trim() === "") return 3000;

    const n = Number(raw);
    if (!Number.isFinite(n) || n <= 0) {
        throw new Error("EF_ENV_PORT_INVALID: PORT must be a positive number");
    }
    return n;
}

function readDbUrl() {
    const raw = process.env.DB_URL;
    if (raw == null || raw.trim() === "") {
        throw new Error("EF_ENV_DB_URL_REQUIRED: DB_URL is required");
    }
    return raw;
}

export const config = {
    port: readPort(),
    dbUrl: readDbUrl()
};
