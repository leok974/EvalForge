import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { workspaceDirFromTestFile, runSh, withRestoredFile } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("FILES is computed (not hardcoded)", async () => {
    // We create a temp file to see if FILES count goes up
    await withRestoredFile(WS, "fixtures/temp_test_file", async () => {
        fs.writeFileSync(path.join(WS, "fixtures/temp_test_file"), "temp");
        const { stdout } = await runSh({ ws: WS });
        assert.match(stdout, /FILES=4/, "EF_CLI_IGNITION_DYNAMIC: expected FILES=4 with extra file");
    });
});
