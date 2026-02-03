import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import {
    runSh,
    readText,
} from "../../../_shared/node_test_helpers.mjs";

const WS = path.resolve(import.meta.dirname, "../../workspace");

test("defaults to dev/3000 when vars missing", async () => {
    await runSh(WS, "task.sh", [], { MODE: undefined, PORT: undefined });
    const out = readText(WS, "outputs/config.txt").trim();
    assert.equal(out, "MODE=dev\nPORT=3000", "EF_CLI_ENV_DEFAULTS: expected defaults");
});

test("uses env vars when provided", async () => {
    await runSh(WS, "task.sh", [], { MODE: "prod", PORT: "8080" });
    const out = readText(WS, "outputs/config.txt").trim();
    assert.equal(out, "MODE=prod\nPORT=8080", "EF_CLI_ENV_USE: expected env values");
});
