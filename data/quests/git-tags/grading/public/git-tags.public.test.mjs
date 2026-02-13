
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-tags", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/tags.txt").trim();
    assert.strictEqual(out, "TAGS=v1.0.0\nTAG_MESSAGE=Release 1.0.0\nHEAD=feat: ship");
});
