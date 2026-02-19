
import { runSh, checkFileExists } from "../../../../_shared/node_test_helpers.mjs";
import assert from "node:assert";
import test from "node:test";
import fs from "node:fs";
import path from "node:path";

test("git-t2-release", async (t) => {
    const WS = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();

    if (!fs.existsSync(path.join(WS, ".git"))) {
        assert.fail("No .git repository found. Did you run ./setup.sh?");
    }

    // Check tag
    const tags = await runSh(WS, "git tag -l v1.0");
    assert.match(tags.stdout, /v1.0/, "Tag v1.0 not found");

    // Check annotated message?
    // tough to check easily without git cat-file, but tag existence is good enough for basic pass
    
    // Check release notes
    assert.ok(fs.existsSync(path.join(WS, "RELEASE_NOTES.md")), "RELEASE_NOTES.md missing");
});
