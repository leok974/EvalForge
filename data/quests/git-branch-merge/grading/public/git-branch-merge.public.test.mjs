
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-branch-merge", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");

    // outputs/parents.txt contains two parent hashes from --no-ff merge commit
    const out = readText(WS, "outputs/parents.txt").trim();
    const parents = out.split(" ").filter(Boolean);
    assert.strictEqual(parents.length, 2, "merge commit should have exactly 2 parents");
    for (const hash of parents) {
        assert.match(hash, /^[0-9a-f]{40}$/, `expected full SHA hash, got: ${hash}`);
    }
});
