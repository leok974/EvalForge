import test from "node:test";
import assert from "node:assert/strict";

import { normalizeConfig } from "../../workspace/task.ts";

test("returns defaults for non-object input", () => {
    assert.deepEqual(
        normalizeConfig(null),
        {
            retries: 3,
            timeoutMs: 500,
            baseUrl: "https://api.local",
            headers: { "x-client": "evalforge" },
        },
        "EF_TS_OBJECTS_DEFAULTS_NULL"
    );
});

test("normalizes and clamps numeric fields", () => {
    assert.deepEqual(
        normalizeConfig({ retries: 999, timeoutMs: 10, baseUrl: "https://x", headers: {} }),
        {
            retries: 10,
            timeoutMs: 50,
            baseUrl: "https://x",
            headers: { "x-client": "evalforge" },
        },
        "EF_TS_OBJECTS_CLAMP"
    );
});

test("rejects non-integer retries/timeoutMs and keeps defaults", () => {
    assert.deepEqual(
        normalizeConfig({ retries: 2.2, timeoutMs: 100.5 }),
        {
            retries: 3,
            timeoutMs: 500,
            baseUrl: "https://api.local",
            headers: { "x-client": "evalforge" },
        },
        "EF_TS_OBJECTS_NONINT"
    );
});

test("trims baseUrl and falls back on empty", () => {
    assert.equal(normalizeConfig({ baseUrl: "  https://api.example " }).baseUrl, "https://api.example", "EF_TS_OBJECTS_URL_TRIM");
    assert.equal(normalizeConfig({ baseUrl: "   " }).baseUrl, "https://api.local", "EF_TS_OBJECTS_URL_EMPTY");
});

test("normalizes headers: lowercase keys, trims values, drops empties", () => {
    const out = normalizeConfig({
        headers: {
            "X-Token": "  abc  ",
            "": "nope",
            "X-Empty": "   ",
            "X-CLIENT": "override",
        },
    });

    assert.deepEqual(
        out.headers,
        {
            "x-client": "override",
            "x-token": "abc",
        },
        "EF_TS_OBJECTS_HEADERS"
    );
});
