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
const DATA = path.join(WS, "fixtures/data.txt");

async function runTask() {
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";
    return execFileAsync(sh, ["task.sh"], { cwd: WS, timeout: 5000 });
}

test("dynamic: uses data.txt contents (not hardcoded)", async () => {
    const orig = fs.readFileSync(DATA, "utf8");
    fs.writeFileSync(DATA, "X\nY\nZ\n", "utf8");
    try {
        await runTask();
        const out = fs.readFileSync(path.join(WS, "outputs/report.txt"), "utf8");
        assert.match(out, /\nX\nY\nZ\n/, "EF_CLI_REDIRECT_DYNAMIC: report must include updated data.txt lines");
    } finally {
        fs.writeFileSync(DATA, orig, "utf8");
    }
});
