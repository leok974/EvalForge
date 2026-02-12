import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { workspaceDirFromTestFile, runSh } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("exits 0 when no flag present", async () => {
    await fs.mkdir(path.join(WS, "fixtures"), { recursive: true });
    try { await fs.unlink(path.join(WS, "fixtures/error.flag")); } catch { }

    const { status, stdout = "", stderr = "" } = await runSh({ ws: WS });
    assert.equal(status, 0, "EF_CLI_EXIT_SUCCESS: must exit 0 when flag missing");
    assert.equal(stdout.trim(), "", "EF_CLI_EXIT_STDOUT_EMPTY: must not print to stdout");
    assert.equal(stderr.trim(), "", "EF_CLI_EXIT_STDERR_EMPTY: must not print to stderr");
});

test("exits 1 when flag present", async () => {
    await fs.mkdir(path.join(WS, "fixtures"), { recursive: true });
    await fs.writeFile(path.join(WS, "fixtures/error.flag"), "");

    try {
        const { status, stdout = "", stderr = "" } = await runSh({ ws: WS });
        assert.equal(status, 1, "EF_CLI_EXIT_FAILURE: must exit 1 when flag exists");
        assert.equal(stdout.trim(), "", "EF_CLI_EXIT_STDOUT_EMPTY: must not print to stdout");
        assert.equal(stderr.trim(), "", "EF_CLI_EXIT_STDERR_EMPTY: must not print to stderr");
    } finally {
        try { await fs.unlink(path.join(WS, "fixtures/error.flag")); } catch { }
    }
});
