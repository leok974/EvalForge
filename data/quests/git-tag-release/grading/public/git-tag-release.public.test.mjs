
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-tag-release", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");

    const out = readText(WS, "outputs/tags.txt").trim();
    assert.strictEqual(out, "v1.0.0", `expected 'v1.0.0' in tags.txt, got: ${out}`);
});
