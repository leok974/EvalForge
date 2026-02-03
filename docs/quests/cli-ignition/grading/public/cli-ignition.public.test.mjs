import test from "node:test";
import assert from "node:assert/strict";
import { workspaceDirFromTestFile, runSh } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("prints exactly CWD, FILES, OK", async () => {
    const { stdout } = await runSh({ ws: WS });

    // Note: CWD might vary based on folder naming (starter vs workspace)
    // The previous test checked for 'starter'. The helper returns path to 'starter'.
    // `task.sh` runs `basename $(pwd)`.
    assert.match(stdout, /CWD=starter/, "EF_CLI_IGNITION_CWD: expected CWD=starter");
    assert.match(stdout, /FILES=3/, "EF_CLI_IGNITION_FILES: expected FILES=3");
    assert.match(stdout, /OK/, "EF_CLI_IGNITION_OK: expected OK");
});
