
import { runSh, runCmd, readText } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";
import fs from "node:fs";
import path from "node:path";

test("git-t2-merge-conflict", async (t) => {
    // EF_WORKSPACE_OVERRIDE is set by run_git_questpack.mjs to the isolated temp workspace
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();

    // Execute the student / solution script (task.sh calls setup.sh then resolves the merge)
    await runSh(WS, "task.sh");

    // .git must exist after setup.sh ran inside task.sh
    assert.ok(
        fs.existsSync(path.join(WS, ".git")),
        "No .git repository found — task.sh must call setup.sh to initialize the repo"
    );

    // Merge commit must appear in log
    const log = await runCmd(WS, "git log --oneline -n 5");
    assert.match(log.stdout, /Merge branch/, "Merge commit not found in log");

    // Conflict markers must be resolved in file.txt
    const content = readText(WS, "file.txt");
    assert.doesNotMatch(content, /<<<<<<<|=======|>>>>>>>/, "Conflict markers still present in file.txt");
});
