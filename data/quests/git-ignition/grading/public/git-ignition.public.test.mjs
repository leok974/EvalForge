
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";
import path from "node:path";
import fs from "node:fs";

test("git-ignition: init + commit", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    // Check outputs/state.txt
    const state = readText(WS, "outputs/state.txt").trim();
    const expected = "BRANCH=main\nCOMMITS=1\nFILES=hello.txt";
    assert.strictEqual(state, expected, "outputs/state.txt mismatch");
});
