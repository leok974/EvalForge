import test from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const wsDir = fileURLToPath(new URL("../../workspace", import.meta.url));

test("learner tests pass and include both test cases", async () => {
    const { stdout, stderr } = await execFileAsync(
        process.execPath,
        ["--test", "tests/math.test.js"],
        { cwd: wsDir, shell: false, encoding: "utf-8" }
    );

    // If tests fail, node --test exits non-zero and execFileAsync throws before here.
    assert.match(stdout, /add correctly adds two numbers/, "EF_NODE_TESTING_HAS_ADD_CASE");
    assert.match(stdout, /subtract correctly subtracts two numbers/, "EF_NODE_TESTING_HAS_SUB_CASE");

    // Keep stderr clean on success (some node versions print minor warnings; allow empty or whitespace)
    assert.ok((stderr ?? "").trim() === "", "EF_NODE_TESTING_STDERR_EMPTY");
});
