import test from "node:test";
import assert from "node:assert/strict";

// NOTE: This import assumes your test runner executes with TS support
// (recommended: node --import tsx --test ...).
import { handshake } from "../../workspace/task.ts";

test("handshake returns the exact typed payload", () => {
    const out = handshake();

    assert.deepEqual(
        out,
        { message: "System Online", code: 42, ok: true },
        "EF_TS_IGN_HANDSHAKE"
    );
});
