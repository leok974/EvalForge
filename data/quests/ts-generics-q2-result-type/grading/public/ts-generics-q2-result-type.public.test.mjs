import test from "node:test";
import assert from "node:assert/strict";
import { success } from "../../workspace/main.ts";

test("success helper", () => {
    const res = success(42);
    assert.equal(res.status, "success");
    if (res.status === "success") {
        assert.equal(res.data, 42); 
    }
});