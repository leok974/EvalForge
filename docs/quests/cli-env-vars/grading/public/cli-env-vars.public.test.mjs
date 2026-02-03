import test from "node:test";
import assert from "node:assert/strict";
import { workspaceDirFromTestFile, runSh, readTextTrim } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("defaults to dev/3000 when vars missing", async () => {
    await runSh({ ws: WS, env: { MODE: undefined, PORT: undefined } });
    const out = readTextTrim(WS, "outputs/config.txt");
    assert.equal(out, "MODE=dev\nPORT=3000", "EF_CLI_ENV_DEFAULTS: expected defaults");
});

test("uses env vars when provided", async () => {
    await runSh({ ws: WS, env: { MODE: "prod", PORT: "8080" } });
    const out = readTextTrim(WS, "outputs/config.txt");
    assert.equal(out, "MODE=prod\nPORT=8080", "EF_CLI_ENV_USE: expected env values");
});
