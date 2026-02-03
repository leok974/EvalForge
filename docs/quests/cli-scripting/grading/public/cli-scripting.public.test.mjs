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

test("copies src to dst when args provided", async () => {
    const src = "fixtures/hello.txt";
    const dst = "outputs/copied.txt";

    await runTask([src, dst]);

    const out = fs.readFileSync(path.join(WS, dst), "utf8");
    assert.equal(out.trimEnd(), "hello world", "EF_CLI_SCRIPT_COPY: expected copied contents");
});

test("prints usage and exits 2 when missing args", async () => {
    try {
        await runTask([]);
        assert.fail("EF_CLI_SCRIPT_EXPECT_EXIT: expected non-zero exit");
    } catch (err) {
        assert.equal(err.code, 2, "EF_CLI_SCRIPT_EXIT_2: expected exit code 2");
        assert.match(String(err.stderr || ""), /Usage:/, "EF_CLI_SCRIPT_USAGE: expected Usage on stderr");
    }
});
