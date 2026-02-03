import test from "node:test";
import assert from "node:assert/strict";
import { workspaceDirFromTestFile, runSh, readTextTrim } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("writes the highest-CPU process line", async () => {
    await runSh({ ws: WS });
    const out = readTextTrim(WS, "outputs/top_cpu.txt");
    assert.equal(out, "202 12 python", "EF_CLI_PROC_TOP: expected highest CPU line");
});
