import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText, writeText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("dynamic: all 200 => OK and 100", async () => {
    writeText(WS, "fixtures/health.txt", "api 200 10\ndb 200 5\ncache 200 1\n");
    await runSh(WS, "task.sh");

    assert.equal(
        norm(readText(WS, "outputs/health_status.txt")),
        "STATUS=OK\nFAILED=\nSLOWEST=api 10",
        "EF_INFRA_HC_OK"
    );
    assert.equal(norm(readText(WS, "outputs/health_score.txt")), "100", "EF_INFRA_HC_OK_SCORE");
});

