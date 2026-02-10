import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("computes degraded status, failures, slowest, and score", async () => {
    await runSh(WS, "task.sh");
    assert.equal(
        norm(readText(WS, "outputs/health_status.txt")),
        "STATUS=DEGRADED\nFAILED=cache\nSLOWEST=api 45",
        "EF_INFRA_HC_STATUS"
    );
    assert.equal(norm(readText(WS, "outputs/health_score.txt")), "66", "EF_INFRA_HC_SCORE");
});

