import test from "node:test";
import assert from "node:assert/strict";
import { waitAndReturn } from "../../workspace/main.js";

test("waitAndReturn returns correct value", async () => {
    const start = Date.now();
    const val = await waitAndReturn(50, "foo");
    const diff = Date.now() - start;
    
    assert.equal(val, "foo");
    assert.ok(diff >= 40, "Should wait approx timeout");
});