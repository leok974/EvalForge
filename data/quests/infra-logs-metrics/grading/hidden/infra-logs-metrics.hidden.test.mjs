import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText, writeText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("dynamic: respects new error frequency", async () => {
    writeText(
        WS,
        "fixtures/app.log",
        "INFO boot\nWARN retry\nERROR E_TIMEOUT\nERROR E_TIMEOUT\nERROR E_TIMEOUT\n"
    );

    await runSh(WS, "task.sh");
    assert.equal(norm(readText(WS, "outputs/top_error.txt")), "E_TIMEOUT", "EF_INFRA_LOGS_DYNAMIC_TOP");
});

