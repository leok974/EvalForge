import test from "node:test";
import assert from "node:assert/strict";
import {
    workspaceDirFromTestFile,
    runSh,
    readTextTrim,
    exists
} from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("writes correct error counts and file list", async () => {
    const { status, stdout, stderr } = await runSh({ ws: WS });

    assert.equal(status, 0, "EF_CLI_GS_EXIT_0: must exit 0");
    assert.equal((stdout ?? "").trim(), "", "EF_CLI_GS_STDOUT_EMPTY: no stdout");
    assert.equal((stderr ?? "").trim(), "", "EF_CLI_GS_STDERR_EMPTY: no stderr");

    assert.ok(exists(WS, "outputs/error_count.txt"), "EF_CLI_GS_COUNT_EXISTS: error_count.txt must exist");
    assert.ok(exists(WS, "outputs/error_files.txt"), "EF_CLI_GS_FILES_EXISTS: error_files.txt must exist");

    const count = readTextTrim(WS, "outputs/error_count.txt");
    const filesRaw = readTextTrim(WS, "outputs/error_files.txt");
    const files = filesRaw ? filesRaw.split("\n").filter(Boolean) : [];

    assert.equal(count, "3", "EF_CLI_GS_COUNT: expected 3 ERROR lines across logs");
    assert.deepEqual(files, ["app.log", "db.log"], "EF_CLI_GS_FILES: expected app.log and db.log");

    // Basename-only sanity (no slashes)
    for (const f of files) {
        if (f.includes("/") || f.includes("\\")) {
            assert.fail(`EF_CLI_GS_BASENAME_ONLY: filenames must not contain directories given: ${f}`);
        }
    }

    // Sorted sanity
    const sorted = [...files].sort((a, b) => a.localeCompare(b));
    assert.deepEqual(files, sorted, "EF_CLI_GS_SORTED: error_files.txt must be sorted");
});
