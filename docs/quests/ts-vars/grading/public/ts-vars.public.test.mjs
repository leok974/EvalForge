import test from "node:test";
import assert from "node:assert/strict";

import { greeting, config } from "../../workspace/task.ts";

test("exports greeting constant", () => {
    assert.equal(greeting, "System Online", "EF_TS_VARS_GREETING");
});

test("exports exact typed config", () => {
    assert.deepEqual(
        config,
        { retryLimit: 3, timeoutMs: 250, env: "dev" },
        "EF_TS_VARS_CONFIG"
    );
});
