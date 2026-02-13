import test from "node:test";
import assert from "node:assert/strict";
import { add } from "../../workspace/main.ts";

test("add function", () => {
    assert.equal(add(10, 5), 15);
});