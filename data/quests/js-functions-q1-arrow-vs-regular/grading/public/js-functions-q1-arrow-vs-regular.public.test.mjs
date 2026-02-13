import test from "node:test";
import assert from "node:assert/strict";
import { add, multiply } from "../../workspace/main.js";

test("add function", () => {
    assert.equal(add(2, 3), 5);
});

test("multiply arrow function", () => {
    assert.equal(multiply(3, 4), 12);
});