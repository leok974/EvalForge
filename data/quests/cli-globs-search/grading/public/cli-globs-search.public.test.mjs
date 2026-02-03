import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import {
    runSh,
    readText,
} from "../../../_shared/node_test_helpers.mjs";

const WS = path.resolve(import.meta.dirname, "../../workspace");

test("writes correct error counts and file list", async () => {
    await runSh(WS);

    const count = readText(WS, "outputs/error_count.txt").trim();
    const files = readText(WS, "outputs/error_files.txt").trim().split("\n").filter(Boolean);

    assert.equal(count, "3", "EF_CLI_GS_COUNT: expected 3 ERROR lines across logs");
    assert.deepEqual(files, ["app.log", "db.log"], "EF_CLI_GS_FILES: expected app.log and db.log");
});
