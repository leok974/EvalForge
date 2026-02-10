import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("splits 0.0.0.0 vs 127.0.0.1 bindings", async () => {
    await runSh(WS, "task.sh");

    assert.equal(
        norm(readText(WS, "outputs/public_ports.txt")),
        "5435 postgres\n8000 uvicorn",
        "EF_INFRA_PORTS_PUBLIC: expected public ports"
    );

    assert.equal(
        norm(readText(WS, "outputs/localhost_ports.txt")),
        "3000 vite\n5173 node",
        "EF_INFRA_PORTS_LOCAL: expected localhost ports"
    );
});

