
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-remote-push", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");

    // outputs/refs.txt contains the branch names present in remote.git/refs/heads/
    const out = readText(WS, "outputs/refs.txt").trim();
    assert.ok(out.includes("main"), `expected 'main' in refs.txt, got: ${out}`);
});
