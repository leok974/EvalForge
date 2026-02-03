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
const INPUT = path.join(WS, "fixtures/input.txt");

async function runTask() {
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";
    return execFileAsync(sh, ["task.sh"], { cwd: WS, timeout: 5000 });
}

test("matches FAIL as whole word only", async () => {
    fs.writeFileSync(INPUT, "FAILURE\nOK\n", "utf8");
    const { stdout } = await runTask();
    assert.equal(stdout.trim(), "OK", "EF_CLI_EXIT_WORD_ONLY: should not fail on FAILURE");
});
