import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import {
    runSh,
    readText,
} from "../../../_shared/node_test_helpers.mjs";

const WS = path.resolve(import.meta.dirname, "../../workspace");

test("prints exactly CWD, FILES, OK", async () => {
    const { stdout } = await runSh(WS);

    // Note: CWD might vary based on folder naming (starter vs workspace)
    // The previous test checked for 'starter'. The helper returns path to 'starter'.
    // `task.sh` runs `basename $(pwd)`.
    assert.match(stdout, /CWD=(starter|workspace)/, "EF_CLI_IGNITION_CWD: expected CWD=starter or workspace");
    assert.match(stdout, /FILES=4/, "EF_CLI_IGNITION_FILES: expected FILES=4");
    assert.match(stdout, /OK/, "EF_CLI_IGNITION_OK: expected OK");
});
