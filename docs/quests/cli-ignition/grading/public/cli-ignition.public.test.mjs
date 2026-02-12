import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, workspaceDirFromTestFile } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);
const expectedCwd = path.basename(WS);

test("prints exactly: CWD, FILES, OK", async () => {
    const { stdout, stderr, status } = await runSh({ ws: WS });

    assert.equal(status, 0, "EF_CLI_IGNITION_EXIT_0: must exit 0");
    assert.equal((stderr ?? "").trim(), "", "EF_CLI_IGNITION_STDERR_EMPTY: no stderr on success");

    const lines = (stdout ?? "").trimEnd().split(/\r?\n/);
    assert.equal(lines.length, 3, "EF_CLI_IGNITION_3_LINES: must print exactly 3 lines");

    assert.equal(lines[0], `CWD=${expectedCwd}`, "EF_CLI_IGNITION_CWD: CWD must match workspace basename");
    assert.equal(lines[1], "FILES=3", "EF_CLI_IGNITION_FILES: must count 3 direct files in fixtures/");
    assert.equal(lines[2], "OK", "EF_CLI_IGNITION_OK: last line must be OK");
});
