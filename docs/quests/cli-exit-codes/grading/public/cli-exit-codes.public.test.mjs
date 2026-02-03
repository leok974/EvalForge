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
const INPUT = path.join(WS, "fixtures/input.txt");

async function runTask() {
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";
    return execFileAsync(sh, ["task.sh"], { cwd: WS, timeout: 5000 });
}

test("prints BAD to stderr and exits 5 when FAIL present", async () => {
    fs.writeFileSync(INPUT, "OK\nFAIL\n", "utf8");
    try {
        await runTask();
        assert.fail("EF_CLI_EXIT_EXPECT_FAIL: expected non-zero exit");
    } catch (err) {
        assert.equal(err.code, 5, "EF_CLI_EXIT_CODE_5: expected exit code 5");
        assert.match(String(err.stderr || ""), /BAD/, "EF_CLI_EXIT_BAD: expected BAD on stderr");
    }
});

test("prints OK and exits 0 when FAIL absent", async () => {
    fs.writeFileSync(INPUT, "OK\nOK\n", "utf8");
    const { stdout, stderr } = await runTask();
    assert.equal(stderr.trim(), "", "EF_CLI_EXIT_STDERR_EMPTY: expected no stderr on success");
    assert.equal(stdout.trim(), "OK", "EF_CLI_EXIT_OK: expected OK on stdout");
});
