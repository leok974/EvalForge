import test from "node:test";
import assert from "node:assert/strict";
import { doubleAll, getEvens, sumAll } from "../../workspace/main.js";

test("doubleAll", () => {
    assert.deepEqual(doubleAll([1, 2]), [2, 4]);
});

test("getEvens", () => {
    assert.deepEqual(getEvens([1, 2, 3, 4]), [2, 4]);
});

test("sumAll", () => {
    assert.equal(sumAll([1, 2, 3]), 6);
});