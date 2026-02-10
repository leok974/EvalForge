import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText, writeText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("uses file values + defaults when env missing", async () => {
    writeText(WS, "fixtures/app.env", "PORT=8000\nLOG_LEVEL=debug\n");

    await runSh(WS, "task.sh", [], { MODE: null, PORT: null, LOG_LEVEL: null });
    assert.equal(
        norm(readText(WS, "outputs/runtime.env")),
        "MODE=dev\nPORT=8000\nLOG_LEVEL=debug",
        "EF_INFRA_ENV_FILE_DEFAULTS"
    );
});

test("env vars override file", async () => {
    writeText(WS, "fixtures/app.env", "PORT=8000\nLOG_LEVEL=debug\n");

    await runSh(WS, "task.sh", [], { MODE: "prod", PORT: "9090" });
    assert.equal(
        norm(readText(WS, "outputs/runtime.env")),
        "MODE=prod\nPORT=9090\nLOG_LEVEL=debug",
        "EF_INFRA_ENV_OVERRIDE"
    );
});

