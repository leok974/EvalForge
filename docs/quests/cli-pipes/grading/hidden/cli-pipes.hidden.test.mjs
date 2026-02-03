import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import { workspaceDirFromTestFile, runSh, readTextTrim, withRestoredFile } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("dynamic: respects new frequencies", async () => {
    await withRestoredFile(WS, "fixtures/names.txt", async (absPath) => {
        fs.writeFileSync(absPath, "maya\nmaya\nmaya\nmaya\n", "utf8");
        await runSh({ ws: WS });
        const out = readTextTrim(WS, "outputs/top.txt");
        assert.match(out, /^maya 4/m, "EF_CLI_PIPES_DYNAMIC: expected maya 4 as top");
    });
});
