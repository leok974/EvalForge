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
const NAMES = path.join(WS, "fixtures/names.txt");

async function runTask() {
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";
    return execFileAsync(sh, ["task.sh"], { cwd: WS, timeout: 5000 });
}

test("dynamic: respects new frequencies", async () => {
    const orig = fs.readFileSync(NAMES, "utf8");
    fs.appendFileSync(NAMES, "\nmaya\nmaya\n", "utf8"); // maya becomes 4
    try {
        await runTask();
        const out = fs.readFileSync(path.join(WS, "outputs/top.txt"), "utf8");
        assert.match(out, /^maya 4/m, "EF_CLI_PIPES_DYNAMIC: expected maya 4 as top");
    } finally {
        fs.writeFileSync(NAMES, orig, "utf8");
    }
});
