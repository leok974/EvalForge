import test from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import path from "node:path";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const starterDir = fileURLToPath(new URL("../../starter", import.meta.url));

test("task.sh prints directory basename and file count", async () => {
    // On Windows, if sh is missing from PATH, fallback to common Git Bash
    // We prefer Git Bash over WSL bash (system32) for consistency in this environment if possible,
    // but C:/Program Files/Git/bin/bash.exe is what we found.
    const shellPath = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";

    try {
        const { stdout } = await execFileAsync(shellPath, ["task.sh"], {
            cwd: starterDir,
            shell: false
        });

        const lines = stdout.trim().split(/\r?\n/);

        // Check 1: Basename
        assert.equal(lines[0], "starter", "EF_CLI_IGNITION_BASENAME: First line should be directory name 'starter'");

        // Check 2: File count
        assert.match(lines[1], /^\d+$/, "EF_CLI_IGNITION_COUNT: Second line should be a number");

    } catch (err) {
        assert.fail(`Execution failed: ${err.message}`);
    }
});
