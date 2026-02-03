import test from "node:test";
import assert from "node:assert/strict";
import {
    workspaceDirFromTestFile,
    runSh,
    readTextTrim,
    writeText,
    withRestoredFile,
} from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("dynamic: respects new ERROR lines", async () => {
    await withRestoredFile(WS, "fixtures/logs/new.log", async () => {
        writeText(WS, "fixtures/logs/new.log", "INFO ok\nERROR boom\n");
        await runSh({ ws: WS });

        const count = readTextTrim(WS, "outputs/error_count.txt");
        const files = readTextTrim(WS, "outputs/error_files.txt");

        assert.equal(count, "4", "EF_CLI_GS_COUNT_DYNAMIC: expected count increase to 4");
        assert.match(files, /new\.log/, "EF_CLI_GS_FILES_DYNAMIC: expected new.log in file list");
    });
});
