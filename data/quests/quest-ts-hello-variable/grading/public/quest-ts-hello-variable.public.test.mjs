import test from "node:test";
import assert from "node:assert/strict";
import * as mod from "../../workspace/main.ts";

test("energy variable", () => {
    assert.equal(typeof mod.energy, "number");
    assert.equal(mod.energy, 100);
});