import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText, writeText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("dynamic: handles added public port", async () => {
    writeText(
        WS,
        "fixtures/netstat.txt",
        "Proto LocalAddress PID Program\n" +
        "tcp 0.0.0.0:9000 111 nginx\n" +
        "tcp 127.0.0.1:5173 222 node\n"
    );

    await runSh(WS, "task.sh");
    assert.equal(norm(readText(WS, "outputs/public_ports.txt")), "9000 nginx", "EF_INFRA_PORTS_DYNAMIC_PUBLIC");
});

