import test from "node:test";
import assert from "node:assert/strict";
import { workspaceDirFromTestFile, runSh, readTextTrim } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("handles empty strings by falling back to defaults", async () => {
    await runSh({ ws: WS, env: { MODE: "", PORT: "" } });
    const out = readTextTrim(WS, "outputs/config.txt");
    assert.equal(out, "MODE=dev\nPORT=3000", "EF_CLI_ENV_EMPTY_DEFAULTS: empty should fall back to defaults");
});
