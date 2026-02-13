import test from "node:test";
import assert from "node:assert/strict";
import * as mod from "../../workspace/main.ts";

test("Types are correct", () => {
    assert.equal(typeof mod.age, "number");
    assert.equal(typeof mod.name, "string");
    assert.equal(typeof mod.isActive, "boolean");
});