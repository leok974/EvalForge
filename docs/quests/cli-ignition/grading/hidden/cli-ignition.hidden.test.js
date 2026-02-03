import test from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import path from "node:path";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const starterDir = fileURLToPath(new URL("../../starter", import.meta.url));

test("task.sh handles extra files correctly", async () => {
    const tempFile = path.join(starterDir, "temp_hidden.txt");
    const fs = await import("node:fs/promises");

    await fs.writeFile(tempFile, "temp");

    const shellPath = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";

    try {
        const { stdout } = await execFileAsync(shellPath, ["task.sh"], {
            cwd: starterDir
        });
        const lines = stdout.trim().split(/\r?\n/);

        const count = parseInt(lines[1], 10);
        assert.ok(count >= 3, "EF_CLI_IGNITION_DYNAMIC: Should count the extra file (>=3)");

    } finally {
        await fs.unlink(tempFile).catch(() => { });
    }
});
