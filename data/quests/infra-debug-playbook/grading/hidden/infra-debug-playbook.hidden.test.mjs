import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText, writeText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("dynamic: CORS symptom produces header steps", async () => {
    writeText(WS, "fixtures/diag.txt", "SYMPTOM=CORS\nAPI_HEALTH=OK\n");
    await runSh(WS, "task.sh");
    const out = norm(readText(WS, "outputs/next_steps.txt"));
    assert.match(out, /Access-Control-Allow-Origin/, "EF_INFRA_DEBUG_CORS_STEP");
});

test("dynamic: unknown symptom falls back to generic steps", async () => {
    writeText(WS, "fixtures/diag.txt", "SYMPTOM=500\nAPI_HEALTH=DOWN\n");
    await runSh(WS, "task.sh");
    assert.equal(
        norm(readText(WS, "outputs/next_steps.txt")),
        "Check health endpoint and status codes\nInspect recent logs for the first error\nValidate config/env and recent deploy changes",
        "EF_INFRA_DEBUG_GENERIC"
    );
});

