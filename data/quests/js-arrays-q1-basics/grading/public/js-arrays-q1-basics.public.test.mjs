import test from "node:test";
import assert from "node:assert/strict";
import { getFirst, getLast, addEnd } from "../../workspace/main.js";

test("Array Access", () => {
    const arr = [10, 20, 30];
    assert.equal(getFirst(arr), 10);
    assert.equal(getLast(arr), 30);
});

test("Array Mutation", () => {
    const arr = [1, 2];
    const newArr = addEnd(arr, 3);
    assert.deepEqual(newArr, [1, 2, 3]);
    // Allow mutation or new array, usually mutation is standard for 'push'
    // But safely return result
});