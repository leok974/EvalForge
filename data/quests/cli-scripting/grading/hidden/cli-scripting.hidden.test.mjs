import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { workspaceDirFromTestFile, runSh, exists } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("creates destination directories if needed", async () => {
    const src = "fixtures/hello.txt";
    const dst = "outputs/nested/dir/copied.txt";

    await runSh({ ws: WS, args: ["task.sh", src, dst] });

    assert.ok(exists(WS, dst), "EF_CLI_SCRIPT_MKDIRP: expected nested dirs created");
});
