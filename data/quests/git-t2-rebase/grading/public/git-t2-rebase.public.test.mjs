
import { runSh } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";
import fs from "node:fs";
import path from "node:path";

test("git-t2-rebase", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();

    if (!fs.existsSync(path.join(WS, ".git"))) {
        assert.fail("No .git repository found. Did you run ./setup.sh?");
    }

    // Check linear history on current branch (should be feature)
    // Counts merge commits
    const merges = await runSh(WS, "git log --merges --oneline");
    assert.strictEqual(merges.stdout.trim(), "", "Found merge commits, history not linear");

    // Check commit C is present in history of feature
    const log = await runSh(WS, "git log --oneline");
    assert.match(log.stdout, /commit C/, "Commit C from main not found in feature history");
    assert.match(log.stdout, /commit D/, "Commit D from feature not found in history");
});
