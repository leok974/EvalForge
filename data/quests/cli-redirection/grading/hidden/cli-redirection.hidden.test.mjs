import test from "node:test";
import assert from "node:assert/strict";
import { workspaceDirFromTestFile, runSh, readTextTrim, writeText, withRestoredFile } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("dynamic: uses data.txt contents (not hardcoded)", async () => {
    await withRestoredFile(WS, "fixtures/data.txt", async () => {
        writeText(WS, "fixtures/data.txt", "X\nY\nZ\n");
        await runSh({ ws: WS });
        const out = readTextTrim(WS, "outputs/report.txt");
        assert.match(out, /\nX\nY\nZ\n/, "EF_CLI_REDIRECT_DYNAMIC: report must include updated data.txt lines");
    });
});
