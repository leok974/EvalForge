import test from "node:test";
import assert from "node:assert/strict";
import { hello } from "../../workspace/main.js";

test("hello() returns correct string", () => {
    assert.equal(hello(), "Hello World");
});