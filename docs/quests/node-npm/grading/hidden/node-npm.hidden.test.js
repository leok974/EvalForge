import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const WS = fileURLToPath(new URL("../../starter/", import.meta.url));

test("check-lockfile fails if package-lock.json missing", async () => {
    const lockPath = path.join(WS, "package-lock.json");
    const tmpPath = path.join(WS, "package-lock.json.__tmp__");

    // If validation environment is shared, this might be risky, but we assume isolation or serialization.
    // We will rename it back in finally.
    // Check if lockfile exists first
    if (!fs.existsSync(lockPath)) return; // Should exist in starter

    fs.renameSync(lockPath, tmpPath);
    try {
        await execFileAsync("npm", ["run", "check-lockfile"], { cwd: WS, shell: true });
        assert.fail("EF_NODE_NPM_LOCKFILE_MISSING: expected non-zero when lockfile missing");
    } catch (err) {
        assert.notEqual(err.code, 0, "EF_NODE_NPM_LOCKFILE_MISSING_CODE: should exit non-zero");
        const stderr = String(err.stderr || "");
        const stdout = String(err.stdout || "");
        assert.match(
            stderr + stdout,
            /package-lock\.json/i,
            "EF_NODE_NPM_LOCKFILE_MISSING_MSG: should mention package-lock.json"
        );
    } finally {
        if (fs.existsSync(tmpPath)) {
            fs.renameSync(tmpPath, lockPath);
        }
    }
});
