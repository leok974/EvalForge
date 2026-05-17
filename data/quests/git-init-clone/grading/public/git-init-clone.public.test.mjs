
import { runSh, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";

test("git-init-clone", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    await runSh(WS, "task.sh");

    const raw = readText(WS, "outputs/report.json").trim();
    const report = JSON.parse(raw);
    assert.strictEqual(report.repo_initialized, true, "repo_initialized should be true");
    assert.strictEqual(report.commit_message, "init", "commit_message should be 'init'");
    assert.strictEqual(report.clone_exists, true, "clone_exists should be true");
});
