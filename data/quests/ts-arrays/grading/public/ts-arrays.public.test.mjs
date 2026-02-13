import test from "node:test";
import assert from "node:assert/strict";
import { sumArray } from "../../workspace/main.ts";

test("sumArray", () => {
    assert.equal(sumArray([1, 2, 3]), 6);
    assert.equal(sumArray([]), 0);
});