
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-log", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/history.txt").trim();
    const expected = "1 chore: init\n2 feat: add api\n3 fix: handle null\n4 docs: update readme";
    assert.strictEqual(out, expected);
});
