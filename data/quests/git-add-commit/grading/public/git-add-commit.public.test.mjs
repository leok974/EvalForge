
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-add-commit", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/commit.txt").trim();
    assert.strictEqual(out, "HEAD=feat: add keep and readme\nTRACKED=2\nUNTRACKED=1");
});
