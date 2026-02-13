
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-undo-revert", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/undo.txt").trim();
    assert.strictEqual(out, "HEAD=revert: bug: wrong value\nVALUE=20\nCOMMITS=4");
});
