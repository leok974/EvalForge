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
const PS = path.join(WS, "fixtures/ps.txt");

async function runTask() {
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";
    return execFileAsync(sh, ["task.sh"], { cwd: WS, timeout: 5000 });
}

test("dynamic: handles different top process", async () => {
    fs.writeFileSync(PS, "PID CPU CMD\n9 99 java\n8 3 node\n", "utf8");
    await runTask();
    const out = fs.readFileSync(path.join(WS, "outputs/top_cpu.txt"), "utf8").trimEnd();
    assert.equal(out, "9 99 java", "EF_CLI_PROC_DYNAMIC: expected java as top");
});
