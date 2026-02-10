import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText, writeText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("dynamic: detects added service", async () => {
    writeText(
        WS,
        "fixtures/docker-compose.yml",
        'version: "3.9"\nservices:\n  api:\n    image: x\n  redis:\n    image: redis\n'
    );

    await runSh(WS, "task.sh");
    assert.equal(norm(readText(WS, "outputs/services.txt")), "api\nredis", "EF_INFRA_DC_DYNAMIC");
});

