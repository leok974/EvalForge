import test from "node:test";
import assert from "node:assert/strict";

import { getUserName } from "../../workspace/src/users.js";

test("getUserName returns name for valid user", async () => {
    const name = await getUserName(10);
    assert.equal(name, "User10", "EF_NODE_ASYNC_SUCCESS");
});

test("getUserName returns 'Guest' on error", async () => {
    const name = await getUserName(-5); // Triggers error in db.js
    assert.equal(name, "Guest", "EF_NODE_ASYNC_ERROR_HANDLING");
});
