import test from "node:test";
import assert from "node:assert/strict";
import { wrap } from "../../workspace/main.ts";

test("wrap generic", () => {
    const n = wrap(10);
    assert.equal(n.value, 10);
    
    const s = wrap("foo");
    assert.equal(s.value, "foo");
});