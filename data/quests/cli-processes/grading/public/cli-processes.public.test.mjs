
import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import {
    runSh,
    readText,
} from "../../../_shared/node_test_helpers.mjs";

const WS = path.resolve(import.meta.dirname, "../../workspace");

test("writes the highest-CPU process line", async () => {
    await runSh(WS);
    const out = readText(WS, "outputs/top_process.txt").trim();
    assert.equal(out, "202 12 python", "EF_CLI_PROC_TOP: expected highest CPU line");
});

