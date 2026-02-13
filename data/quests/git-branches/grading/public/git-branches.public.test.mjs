
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-branches", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/branches.txt").trim();
    assert.strictEqual(out, "CURRENT=main\nMAIN_HEAD=chore: base\nFEATURE_HEAD=feat: ui tweak");
});
