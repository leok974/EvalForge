
import { runSh, runCmd } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";
import fs from "node:fs";
import path from "node:path";

test("git-t2-rebase", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();

    // Execute the student / solution script
    await runSh(WS, "task.sh");

    assert.ok(
        fs.existsSync(path.join(WS, ".git")),
        "No .git repository found — task.sh must call setup.sh to initialize the repo"
    );

    // History must be linear (no merge commits) after the rebase
    const merges = await runCmd(WS, "git log --merges --oneline");
    assert.strictEqual(merges.stdout.trim(), "", "Found merge commits — history should be linear after rebase");

    // Commit C (from main) and Commit D (from feature) must both be present
    const log = await runCmd(WS, "git log --oneline");
    assert.match(log.stdout, /commit C/, "Commit C from main not found in feature history after rebase");
    assert.match(log.stdout, /commit D/, "Commit D from feature not found in history after rebase");
});
