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

async function runTask(args = []) {
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";
    return execFileAsync(sh, ["task.sh", ...args], { cwd: WS, timeout: 5000 });
}

test("creates destination directories if needed", async () => {
    const src = "fixtures/hello.txt";
    const dst = "outputs/nested/dir/copied.txt";

    await runTask([src, dst]);

    assert.ok(fs.existsSync(path.join(WS, dst)), "EF_CLI_SCRIPT_MKDIRP: expected nested dirs created");
});
