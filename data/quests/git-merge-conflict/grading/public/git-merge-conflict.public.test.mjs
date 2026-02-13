
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-merge-conflict", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/merge.txt").trim();
    assert.strictEqual(out, "STATUS=OK\nHEAD=merge: feature/a\nCONFIG=MODE=main+feature");
});
