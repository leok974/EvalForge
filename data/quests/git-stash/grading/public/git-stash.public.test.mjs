
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-stash", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/stash.txt").trim();
    assert.strictEqual(out, "STASHED=1\nCLEAN_AFTER_STASH=1\nRESTORED_WIP=work\nRESTORED_TMP=scratch");
});
