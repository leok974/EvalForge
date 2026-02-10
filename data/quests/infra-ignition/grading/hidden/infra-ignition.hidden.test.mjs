import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText, writeText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n");

test("passes when all tools are installed (dynamic)", async () => {
    writeText(WS, "fixtures/tools.txt", "docker\ngit\nnode\n");
    writeText(WS, "fixtures/which.txt", "docker\ngit\nnode\n");

    await runSh(WS, "task.sh");
    const out = norm(readText(WS, "outputs/preflight.txt"));
    assert.equal(out, "STATUS=OK\nMISSING=", "EF_INFRA_IGN_OK: expected OK + empty missing");
});

