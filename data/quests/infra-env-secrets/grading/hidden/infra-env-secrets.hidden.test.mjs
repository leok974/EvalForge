import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("output contains only the required three lines", async () => {
    const { stdout } = await execFileAsync(process.execPath, ["check_env.js"], {
        cwd: WS,
        env: { ...process.env, API_KEY: "ok" },
        timeout: 5000
    });
    const lines = stdout.trimEnd().split("\n").filter(Boolean);
    assert.equal(lines.length, 3, "EF_INFRA_ENV_LINES: must print exactly 3 lines");
});
