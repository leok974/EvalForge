import test from "node:test";
import assert from "node:assert/strict";
import run, { CONFIG } from "../../workspace/main.ts";

test("Exports check", () => {
    assert.equal(CONFIG.env, "dev");
    assert.equal(run(), "Running in dev");
});