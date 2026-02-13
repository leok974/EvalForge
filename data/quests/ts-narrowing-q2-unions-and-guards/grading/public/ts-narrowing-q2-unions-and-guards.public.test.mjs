import test from "node:test";
import assert from "node:assert/strict";
import { format } from "../../workspace/main.ts";

test("format logic", () => {
    assert.equal(format(10), "Value: 10");
    assert.equal(format("hello"), "HELLO");
});