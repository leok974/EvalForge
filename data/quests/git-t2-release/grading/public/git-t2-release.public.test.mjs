
import { runSh, runCmd } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";
import fs from "node:fs";
import path from "node:path";

test("git-t2-release", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();

    // Execute the student / solution script
    await runSh(WS, "task.sh");

    assert.ok(
        fs.existsSync(path.join(WS, ".git")),
        "No .git repository found — task.sh must call setup.sh to initialize the repo"
    );

    // Annotated tag v1.0 must exist
    const tags = await runCmd(WS, "git tag -l v1.0");
    assert.match(tags.stdout, /v1.0/, "Tag v1.0 not found — use: git tag -a v1.0 -m 'Release 1.0'");

    // RELEASE_NOTES.md must be present in workspace
    assert.ok(
        fs.existsSync(path.join(WS, "RELEASE_NOTES.md")),
        "RELEASE_NOTES.md missing from workspace — create and commit the file"
    );
});
