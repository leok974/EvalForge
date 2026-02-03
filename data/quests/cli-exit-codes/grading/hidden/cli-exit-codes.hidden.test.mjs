import test from "node:test";
import assert from "node:assert/strict";
import {
    workspaceDirFromTestFile,
    runSh,
    writeText,
    withRestoredFile
} from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("matches FAIL as whole word only", async () => {
    await withRestoredFile(WS, "fixtures/input.txt", async () => {
        writeText(WS, "fixtures/input.txt", "FAILURE\nOK\n");
        const { stdout } = await runSh({ ws: WS });
        assert.equal(stdout.trim(), "OK", "EF_CLI_EXIT_WORD_ONLY: should not fail on FAILURE");
    });
});
