import test from "node:test";
import assert from "node:assert/strict";
import { hello } from "../../workspace/main.ts";

test("hello returns greeting", () => {
    assert.equal(hello("World"), "Hello, World!");
    assert.equal(hello("EvalForge"), "Hello, EvalForge!");
});