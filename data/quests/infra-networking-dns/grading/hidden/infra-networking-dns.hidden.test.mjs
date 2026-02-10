import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText, writeText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("dynamic: respects new mapping", async () => {
    writeText(WS, "fixtures/hosts.txt", "127.0.0.1 api.local\n10.0.0.6 cache.local\n");
    writeText(WS, "fixtures/requests.txt", "cache.local\napi.local\n");

    await runSh(WS, "task.sh");
    assert.equal(norm(readText(WS, "outputs/resolved.txt")), "cache.local 10.0.0.6\napi.local 127.0.0.1", "EF_INFRA_DNS_DYNAMIC");
});

