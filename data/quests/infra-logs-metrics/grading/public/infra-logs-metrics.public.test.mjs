import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("computes log counters and top error", async () => {
    await runSh(WS, "task.sh");

    const prom = norm(readText(WS, "outputs/metrics.prom"));
    assert.match(prom, /^app_log_info_total 1$/m, "EF_INFRA_LOGS_INFO");
    assert.match(prom, /^app_log_warnings_total 1$/m, "EF_INFRA_LOGS_WARN");
    assert.match(prom, /^app_log_errors_total 3$/m, "EF_INFRA_LOGS_ERR");

    assert.equal(norm(readText(WS, "outputs/top_error.txt")), "E_CONNREFUSED", "EF_INFRA_LOGS_TOP");
});

