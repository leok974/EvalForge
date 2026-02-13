import test from "node:test";
import assert from "node:assert/strict";
import * as mod from "../../workspace/main.js"; // Import namespace to check exports

test("Exports exist and are correct types", () => {
    assert.equal(typeof mod.age, "number");
    assert.equal(typeof mod.NAME, "string");
    assert.equal(typeof mod.isStudent, "boolean");
});

test("NAME is constant convention", () => {
    assert.equal(mod.NAME, "EvalForge");
});