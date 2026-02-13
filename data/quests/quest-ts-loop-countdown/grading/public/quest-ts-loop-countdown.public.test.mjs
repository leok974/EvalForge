import test from "node:test";
import assert from "node:assert/strict";
import { countdown } from "../../workspace/main.ts";

test("countdown logic", () => {
    assert.deepEqual(countdown(3), [3, 2, 1, 0]);
    assert.deepEqual(countdown(0), [0]);
});