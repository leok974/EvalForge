import test from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import path from "node:path";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const starterDir = fileURLToPath(new URL("../../starter", import.meta.url));

test("task.sh navigates to correct directory", async () => {
    const shellPath = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";

    try {
        const { stdout } = await execFileAsync(shellPath, ["task.sh"], {
            cwd: starterDir,
            shell: false
        });
        
        const lines = stdout.trim().split(/\r?\n/);
        const lastLine = lines[lines.length - 1]; // PWD should be last
        
        // We expect path ending in fixtures/site/ops/logs
        // We normalize separators to / for checking
        const normalized = lastLine.replace(/\\/g, "/");
        
        assert.match(normalized, /fixtures\/site\/ops\/logs$/, "EF_CLI_NAV_PATH: Output should end with .../fixtures/site/ops/logs");
        
    } catch (err) {
        assert.fail(`Execution failed: ${err.message}`);
    }
});
