import test from "node:test";
import assert from "node:assert/strict";

import { isUser, parseUser } from "../../workspace/task.ts";

test("isUser returns true for valid user objects", () => {
    assert.equal(
        isUser({ id: 1, name: "Ada", role: "admin" }),
        true,
        "EF_TS_TYPES_GUARD_TRUE"
    );
});

test("isUser returns false for invalid shapes", () => {
    assert.equal(isUser(null), false, "EF_TS_TYPES_GUARD_NULL");
    assert.equal(isUser({ id: "1", name: "Ada", role: "admin" }), false, "EF_TS_TYPES_GUARD_ID");
    assert.equal(isUser({ id: 1, name: 123, role: "admin" }), false, "EF_TS_TYPES_GUARD_NAME");
    assert.equal(isUser({ id: 1, name: "Ada", role: "root" }), false, "EF_TS_TYPES_GUARD_ROLE");
});

test("parseUser returns user for valid JSON", () => {
    const u = parseUser('{"id":2,"name":"Grace","role":"user"}');
    assert.deepEqual(u, { id: 2, name: "Grace", role: "user" }, "EF_TS_TYPES_PARSE_OK");
});

test("parseUser throws EF_TS_TYPES_INVALID on invalid JSON", () => {
    assert.throws(
        () => parseUser("{not json"),
        (err) => err instanceof Error && err.message === "EF_TS_TYPES_INVALID",
        "EF_TS_TYPES_PARSE_BAD_JSON"
    );
});

test("parseUser throws EF_TS_TYPES_INVALID on invalid shape", () => {
    assert.throws(
        () => parseUser('{"id":"2","name":"Grace","role":"user"}'),
        (err) => err instanceof Error && err.message === "EF_TS_TYPES_INVALID",
        "EF_TS_TYPES_PARSE_BAD_SHAPE"
    );
});
