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
const LOGS = path.join(WS, "fixtures/logs");

async function runTask() {
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";
    return execFileAsync(sh, ["task.sh"], { cwd: WS, timeout: 5000 });
}

test("dynamic: respects new ERROR lines", async () => {
    const p = path.join(LOGS, "new.log");
    fs.writeFileSync(p, "INFO ok\nERROR boom\n", "utf8");
    try {
        await runTask();
        const count = fs.readFileSync(path.join(WS, "outputs/error_count.txt"), "utf8").trim();
        const files = fs.readFileSync(path.join(WS, "outputs/error_files.txt"), "utf8");
        assert.equal(count, "4", "EF_CLI_GS_COUNT_DYNAMIC: expected count increase to 4");
        assert.match(files, /new\.log/, "EF_CLI_GS_FILES_DYNAMIC: expected new.log in file list");
    } finally {
        fs.unlinkSync(p);
    }
});
