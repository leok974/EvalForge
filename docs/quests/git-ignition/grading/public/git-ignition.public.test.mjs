import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";

// We assume the runner runs this test with CWD = workspace root (or we find it)
// But for uniformity with CLI/TS runners, let's use `process.cwd()` or `EF_WORKSPACE_OVERRIDE`

const workspace = process.env.EF_WORKSPACE_OVERRIDE || process.cwd();

test("repository is initialized", () => {
    const gitDir = path.join(workspace, ".git");
    assert.ok(fs.existsSync(gitDir), "EF_GIT_IGNITION_NO_GIT_DIR");

    // Safety check: is it a valid repo?
    try {
        execSync("git status", { cwd: workspace, stdio: "ignore" });
    } catch {
        assert.fail("EF_GIT_IGNITION_GIT_STATUS_FAILED");
    }
});
