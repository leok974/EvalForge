import test from "node:test";
import assert from "node:assert/strict";
import { workspaceDirFromTestFile, runSh } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("prints usage and exits 1 when no args", async () => {
    const { status, stdout = "", stderr = "" } = await runSh({ ws: WS });
    assert.equal(status, 1, "EF_CLI_SCRIPT_EXIT_1: expected exit code 1");
    assert.equal(stderr.trim(), "", "EF_CLI_SCRIPT_STDERR_EMPTY: keep stderr empty");
    assert.equal(stdout.trimEnd(), "Usage: task.sh <name>", "EF_CLI_SCRIPT_USAGE: expected usage message");
});

test("prints usage and exits 1 when blank arg", async () => {
    const { status, stdout = "", stderr = "" } = await runSh({ ws: WS, args: ["   "] });
    assert.equal(status, 1, "EF_CLI_SCRIPT_EXIT_1_BLANK: expected exit code 1");
    assert.equal(stderr.trim(), "", "EF_CLI_SCRIPT_STDERR_EMPTY: keep stderr empty");
    assert.equal(stdout.trimEnd(), "Usage: task.sh <name>", "EF_CLI_SCRIPT_USAGE_BLANK: expected usage");
});

test("greets name and exits 0", async () => {
    const { status, stdout = "", stderr = "" } = await runSh({ ws: WS, args: ["World"] });
    assert.equal(status, 0, "EF_CLI_SCRIPT_SUCCESS: expected exit 0");
    assert.equal(stderr.trim(), "", "EF_CLI_SCRIPT_STDERR_EMPTY: keep stderr empty");
    assert.equal(stdout.trimEnd(), "Hello, World!", "EF_CLI_SCRIPT_GREET: expected greeting");
});
