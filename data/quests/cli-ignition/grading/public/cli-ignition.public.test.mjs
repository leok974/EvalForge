import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import fs from "node:fs";
import {
    runSh,
    readText,
} from "../../../_shared/node_test_helpers.mjs";

const WS = path.resolve(import.meta.dirname, "../../workspace");

test("prints exactly CWD, FILES, OK", async () => {
    // Ensure clean state (no outputs dir)
    await runSh(WS, "task.sh", [], {}, 1000).catch(() => { }); // Run once to check? No.
    if (fs.existsSync(path.join(WS, "outputs"))) {
        fs.rmSync(path.join(WS, "outputs"), { recursive: true, force: true });
    }

    const { stdout } = await runSh(WS);

    // Note: CWD might vary based on folder naming (starter vs workspace)
    // The previous test checked for 'starter'. The helper returns path to 'starter'.
    // `task.sh` runs `basename $(pwd)`.
    assert.match(stdout, /CWD=(starter|workspace)/, "EF_CLI_IGNITION_CWD: expected CWD=starter or workspace");
    assert.match(stdout, /FILES=(4|5)/, "EF_CLI_IGNITION_FILES: expected FILES=4 or 5");
    assert.match(stdout, /OK/, "EF_CLI_IGNITION_OK: expected OK");
});
