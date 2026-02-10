import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("502 produces reverse-proxy oriented next steps", async () => {
    await runSh(WS, "task.sh");
    assert.equal(
        norm(readText(WS, "outputs/next_steps.txt")),
        "Check reverse proxy upstream host/port\nVerify backend /health from proxy network\nInspect backend logs for crash/restarts",
        "EF_INFRA_DEBUG_502"
    );
});

