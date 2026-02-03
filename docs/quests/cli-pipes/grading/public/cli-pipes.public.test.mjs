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

test("top.txt contains top 2 names with counts", async () => {
    await runTask();
    const out = fs.readFileSync(path.join(WS, "outputs/top.txt"), "utf8").trimEnd().split("\n");
    assert.deepEqual(out, ["leo 3", "maya 2"], "EF_CLI_PIPES_TOP2: expected 'leo 3' then 'maya 2'");
});
