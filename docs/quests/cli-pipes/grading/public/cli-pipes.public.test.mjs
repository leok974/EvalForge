import test from "node:test";
import assert from "node:assert/strict";
import { workspaceDirFromTestFile, runSh, readTextTrim, exists } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("top.txt contains top 2 names with counts", async () => {
    const { status, stdout, stderr } = await runSh({ ws: WS });

    assert.equal(status, 0, "EF_CLI_PIPES_EXIT_0: must exit 0");
    assert.equal((stdout ?? "").trim(), "", "EF_CLI_PIPES_STDOUT_EMPTY: no stdout");
    assert.equal((stderr ?? "").trim(), "", "EF_CLI_PIPES_STDERR_EMPTY: no stderr");

    assert.ok(exists(WS, "outputs/top.txt"), "EF_CLI_PIPES_TOP_EXISTS: outputs/top.txt must exist");

    const out = readTextTrim(WS, "outputs/top.txt")
        .split("\n")
        .filter(Boolean);

    assert.deepEqual(out, ["leo 3", "maya 2"], "EF_CLI_PIPES_TOP2: expected 'leo 3' then 'maya 2'");
});
