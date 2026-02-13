import test from "node:test";
import assert from "node:assert/strict";
import { checkNumber, sumTo } from "../../workspace/main.js";

test("checkNumber", () => {
    assert.equal(checkNumber(10), "positive");
    assert.equal(checkNumber(-5), "negative");
    assert.equal(checkNumber(0), "zero");
});

test("sumTo", () => {
    assert.equal(sumTo(5), 15); // 1+2+3+4+5
    assert.equal(sumTo(1), 1);
    assert.equal(sumTo(0), 0);
});