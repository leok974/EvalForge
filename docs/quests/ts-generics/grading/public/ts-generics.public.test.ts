import test from "node:test";
import assert from "node:assert/strict";

import { pick } from "../../workspace/task.ts";

test("picks requested keys from an object", () => {
    const user = { id: 1, name: "Ada", role: "admin", active: true };

    const out = pick(user, ["id", "name"]);
    assert.deepEqual(out, { id: 1, name: "Ada" }, "EF_TS_GEN_PICK_BASIC");
});

test("does not mutate the original object", () => {
    const obj = { a: 1, b: 2, c: 3 };
    const out = pick(obj, ["b"]);

    assert.deepEqual(out, { b: 2 }, "EF_TS_GEN_PICK_OUT");
    assert.deepEqual(obj, { a: 1, b: 2, c: 3 }, "EF_TS_GEN_NO_MUTATION");
});

test("preserves key insertion order from the keys array", () => {
    const obj = { a: 1, b: 2, c: 3 };
    const out = pick(obj, ["c", "a"]);

    assert.deepEqual(out, { c: 3, a: 1 }, "EF_TS_GEN_ORDER");
});
