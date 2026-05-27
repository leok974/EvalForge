
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-rebase-linear", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");

    // outputs/log.txt is `git log --oneline` — 3 commits in linear order
    const out = readText(WS, "outputs/log.txt").trim();
    assert.ok(out.includes("Feature commit"), `expected 'Feature commit' in log.txt, got: ${out}`);
    assert.ok(out.includes("Main update"), `expected 'Main update' in log.txt, got: ${out}`);
    assert.ok(out.includes("Root commit"), `expected 'Root commit' in log.txt, got: ${out}`);

    // Verify linear history: Feature commit should appear before Main update (newer first)
    const lines = out.split("\n").filter(Boolean);
    const featureIdx = lines.findIndex(l => l.includes("Feature commit"));
    const mainIdx = lines.findIndex(l => l.includes("Main update"));
    assert.ok(featureIdx < mainIdx, "Feature commit should appear before Main update in log (newer first)");
    assert.strictEqual(lines.length, 3, `expected 3 commits, got ${lines.length}`);
});
