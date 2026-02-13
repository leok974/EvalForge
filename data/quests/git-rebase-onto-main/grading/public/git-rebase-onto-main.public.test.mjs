
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-rebase-onto-main", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");
    
    const out = readText(WS, "outputs/rebase.txt").trim();
    assert.strictEqual(out, "ORDER=chore: base|hotfix: patch|feat: one|feat: two\nBRANCH=feature/x\nBASE=main");
});
