import test from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import path from "node:path";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const WS = path.resolve(__dirname, "../../starter"); // NOTE: Modified from "../../workspace" to "../../starter" to match our layout

async function runTask() {
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";
    return execFileAsync(sh, ["task.sh"], { cwd: WS, timeout: 5000 });
}

test("prints exactly CWD, FILES, OK", async () => {
    const { stdout, stderr } = await runTask();

    assert.equal(stderr.trim(), "", "EF_CLI_IGNITION_STDERR_EMPTY: should not write to stderr");

    const lines = stdout.trimEnd().split("\n");
    assert.equal(lines.length, 3, "EF_CLI_IGNITION_LINES: expected exactly 3 lines of output");

    assert.equal(lines[0], "CWD=starter", "EF_CLI_IGNITION_CWD: expected CWD=starter"); // NOTE: Modified expected CWD from workspace to starter
    assert.equal(lines[1], "FILES=3", "EF_CLI_IGNITION_FILES: expected FILES=3 (regular files only)");
    assert.equal(lines[2], "OK", "EF_CLI_IGNITION_OK: expected OK");
});
