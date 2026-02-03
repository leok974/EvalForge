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

async function runTask(env) {
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";
    return execFileAsync(sh, ["task.sh"], { cwd: WS, env: { ...process.env, ...env }, timeout: 5000 });
}

test("handles empty strings by falling back to defaults", async () => {
    await runTask({ MODE: "", PORT: "" });
    const out = fs.readFileSync(path.join(WS, "outputs/config.txt"), "utf8").trimEnd();
    assert.equal(out, "MODE=dev\nPORT=3000", "EF_CLI_ENV_EMPTY_DEFAULTS: empty should fall back to defaults");
});
