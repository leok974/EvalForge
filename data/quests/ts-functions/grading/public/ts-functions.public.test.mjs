import test from "node:test";
import assert from "node:assert/strict";
import { greet } from "../../workspace/main.ts";

test("greet logic", () => {
    assert.equal(greet("Alice"), "Hello, Alice");
    assert.equal(greet("Bob", "Dr."), "Hello, Dr. Bob");
});