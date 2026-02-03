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

async function runTask() {
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";
    return execFileAsync(sh, ["task.sh"], { cwd: WS, timeout: 5000 });
}
const read = (rel) => fs.readFileSync(path.join(WS, rel), "utf8").trimEnd();

test("writes correct error counts and file list", async () => {
    await runTask();

    const count = read("outputs/error_count.txt");
    const files = read("outputs/error_files.txt").split("\n").filter(Boolean);

    assert.equal(count, "3", "EF_CLI_GS_COUNT: expected 3 ERROR lines across logs");
    assert.deepEqual(files, ["app.log", "db.log"], "EF_CLI_GS_FILES: expected app.log and db.log");
});
