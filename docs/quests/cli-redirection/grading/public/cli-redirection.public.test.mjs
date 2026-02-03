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
const read = (rel) => fs.readFileSync(path.join(WS, rel), "utf8").replace(/\r\n/g, "\n").trimEnd();

test("report contains header + data + footer", async () => {
    await runTask();
    const lines = read("outputs/report.txt").split("\n");
    assert.equal(lines[0], "HEADER", "EF_CLI_REDIRECT_HEADER: first line must be HEADER");
    assert.equal(lines.at(-1), "FOOTER", "EF_CLI_REDIRECT_FOOTER: last line must be FOOTER");
    assert.equal(lines.slice(1, -1).join("\n"), read("fixtures/data.txt"), "EF_CLI_REDIRECT_BODY: middle must match fixtures/data.txt");
});
