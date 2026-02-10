import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, writeText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("invalid PORT exits 12 and prints error code", async () => {
    writeText(WS, "fixtures/app.env", "PORT=notanumber\nLOG_LEVEL=info\n");
    try {
        await runSh(WS, "task.sh", [], { PORT: null });
        assert.fail("EF_INFRA_ENV_EXPECT_FAIL: expected exit 12");
    } catch (err) {
        assert.equal(err.code, 12, "EF_INFRA_ENV_EXIT12");
        assert.match(String(err.stderr || ""), /EF_INFRA_ENV_PORT_INVALID/, "EF_INFRA_ENV_STDERR_CODE");
    }
});

