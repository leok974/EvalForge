import test from "node:test";
import assert from "node:assert/strict";

import { formatEvent } from "../../workspace/task.ts";

test("formats base events", () => {
    const out = formatEvent({ id: "evt_9", ts: 1700000009999, type: "system.boot" });
    assert.equal(out, "system.boot id=evt_9 ts=1700000009999", "EF_TS_IF_BASE");
});

test("formats user events with userId", () => {
    const out = formatEvent({
        id: "evt_1",
        ts: 1700000000000,
        type: "user.login",
        userId: "u1",
    });

    assert.equal(out, "user.login id=evt_1 ts=1700000000000 user=u1", "EF_TS_IF_USER");
});

test("formats user events with ip when present", () => {
    const out = formatEvent({
        id: "evt_2",
        ts: 1700000001234,
        type: "user.logout",
        userId: "u7",
        ip: "127.0.0.1",
    });

    assert.equal(
        out,
        "user.logout id=evt_2 ts=1700000001234 user=u7 ip=127.0.0.1",
        "EF_TS_IF_IP"
    );
});
