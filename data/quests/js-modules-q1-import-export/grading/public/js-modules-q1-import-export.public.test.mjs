import test from "node:test";
import assert from "node:assert/strict";
import circleArea, { PI, E } from "../../workspace/main.js";

test("Named exports", () => {
    assert.equal(PI, 3.14159);
    assert.equal(E, 2.718);
});

test("Default export circleArea", () => {
    assert.ok(Math.abs(circleArea(1) - 3.14159) < 0.0001);
});