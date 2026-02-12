import test from "node:test";
import assert from "node:assert/strict";
import { workspaceDirFromTestFile, runSh, readTextTrim } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("extracts python PIDs (sorted) into outputs/pids.txt", async () => {
    const { status, stdout = "", stderr = "" } = await runSh({ ws: WS });
    assert.equal(status, 0, "EF_CLI_PROC_EXIT_0: script must exit 0");
    assert.equal(stdout.trim(), "", "EF_CLI_PROC_STDOUT_EMPTY: no stdout");
    assert.equal(stderr.trim(), "", "EF_CLI_PROC_STDERR_EMPTY: no stderr");

    const pids = readTextTrim(WS, "outputs/pids.txt").split("\n").filter(Boolean);
    assert.deepEqual(pids, ["102", "104"], "EF_CLI_PROC_PIDS: expected python PIDs 102 and 104 (sorted)");
});
