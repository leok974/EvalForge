
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-status-diff", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const status = readText(WS, "outputs/status.txt").trim();
    assert.strictEqual(status, "STAGED=1\nMODIFIED=0\nUNTRACKED=1", "status.txt mismatch");
    
    const diff = readText(WS, "outputs/diff.txt").trim();
    assert.strictEqual(diff, "app.txt: v1 -> v2", "diff.txt mismatch");
});
