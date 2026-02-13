import test from "node:test";
import assert from "node:assert/strict";
import { getUser } from "../../workspace/main.ts";

test("getUser returns typed object", () => {
    const u = getUser(1, "alice");
    assert.equal(u.id, 1);
    assert.equal(u.username, "alice");
});