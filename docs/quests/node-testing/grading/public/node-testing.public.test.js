import test from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const starterDir = fileURLToPath(new URL("../../starter", import.meta.url));

test("npm test passes", async () => {
    // We run the user's tests. If they implemented assertions correctly, it exits 0.
    // If they left it empty, node test might pass if no assertions fail, 
    // BUT we want to ensure they *added* assertions. 
    // Actually, empty tests pass in node:test.
    // We need to check if the output contains "pass 2".

    const { stdout } = await execFileAsync(process.execPath, ["--test", "tests/math.test.js"], {
        cwd: starterDir,
        shell: false
    });

    assert.match(stdout, /pass 2/, "EF_TEST_PASS_COUNT: Should pass 2 tests");
});
