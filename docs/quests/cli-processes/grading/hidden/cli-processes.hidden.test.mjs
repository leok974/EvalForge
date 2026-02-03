import test from "node:test";
import assert from "node:assert/strict";
import {
    workspaceDirFromTestFile,
    runSh,
    readTextTrim,
    writeText,
    withRestoredFile
} from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("dynamic: handles different top process", async () => {
    await withRestoredFile(WS, "fixtures/ps.txt", async () => {
        writeText(WS, "fixtures/ps.txt", "PID CPU CMD\n9 99 java\n8 3 node\n");
        await runSh({ ws: WS });
        const out = readTextTrim(WS, "outputs/top_cpu.txt");
        assert.equal(out, "9 99 java", "EF_CLI_PROC_DYNAMIC: expected java as top");
    });
});
