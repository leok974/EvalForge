import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const WS = path.resolve(__dirname, "../../starter"); // NOTE: Modified
const FIXT = path.join(WS, "fixtures");

async function runTask() {
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";
    return execFileAsync(sh, ["task.sh"], { cwd: WS, timeout: 5000 });
}

test("FILES is computed (not hardcoded)", async () => {
    const extra = path.join(FIXT, "extra.tmp");
    fs.writeFileSync(extra, "x", "utf8");

    try {
        const { stdout } = await runTask();
        const lines = stdout.trimEnd().split("\n");
        assert.equal(lines[1], "FILES=4", "EF_CLI_IGNITION_FILES_DYNAMIC: expected FILES=4 after adding a file");
    } finally {
        fs.unlinkSync(extra);
    }
});
