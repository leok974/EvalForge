import test from "node:test";
import assert from "node:assert/strict";
import {
    workspaceDirFromTestFile,
    runSh,
    readTextTrim,
} from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("writes correct error counts and file list", async () => {
    await runSh({ ws: WS });

    const count = readTextTrim(WS, "outputs/error_count.txt");
    const files = readTextTrim(WS, "outputs/error_files.txt").split("\n").filter(Boolean);

    assert.equal(count, "3", "EF_CLI_GS_COUNT: expected 3 ERROR lines across logs");
    assert.deepEqual(files, ["app.log", "db.log"], "EF_CLI_GS_FILES: expected app.log and db.log");
});
