
import { runSh, readText, checkFileExists } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";
import fs from "node:fs";
import path from "node:path";

test("git-t2-merge-conflict", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();
    
    // Check clean status
    // We assume the user ran setup.sh and did work.
    // If .git missing, fail
    if (!fs.existsSync(path.join(WS, ".git"))) {
        assert.fail("No .git repository found. Did you run ./setup.sh?");
    }

    // Check merge commit
    const log = await runSh(WS, "git log --oneline -n 5");
    assert.match(log.stdout, /Merge branch/, "Merge commit not found in log");

    // Check conflict markers gone
    const content = readText(WS, "file.txt");
    assert.doesNotMatch(content, /<<<<<<<|=======|>>>>>>>/, "Conflict markers found in file.txt");
});
