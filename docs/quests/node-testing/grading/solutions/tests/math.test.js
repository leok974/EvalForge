import test from "node:test";
import assert from "node:assert/strict";
import { add, subtract } from "../src/math.js";

test("add correctly adds two numbers", () => {
    assert.equal(add(2, 3), 5);
});

test("subtract correctly subtracts two numbers", () => {
    assert.equal(subtract(5, 2), 3);
});
