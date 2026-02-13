import test from "node:test";
import assert from "node:assert/strict";
import { Circle } from "../../workspace/main.ts";

test("Circle implements Shape", () => {
    const c = new Circle(10);
    // Area = pi * r^2 ~= 314.159
    assert.ok(Math.abs(c.area() - 314.159) < 0.01);
});