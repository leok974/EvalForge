import test from "node:test";
import assert from "node:assert/strict";
import { workspaceDirFromTestFile, runSh, readTextTrim } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("top.txt contains top 2 names with counts", async () => {
    await runSh({ ws: WS });
    const out = readTextTrim(WS, "outputs/top.txt").split("\n");
    assert.deepEqual(out, ["leo 3", "maya 2"], "EF_CLI_PIPES_TOP2: expected 'leo 3' then 'maya 2'");
});
