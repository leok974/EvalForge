import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText, writeText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

const norm = (s) => s.replace(/\r\n/g, "\n");

test("fails preflight when a required tool is missing", async () => {
    writeText(WS, "fixtures/tools.txt", "docker\ngit\nnode\n");
    writeText(WS, "fixtures/which.txt", "docker\nnode\n");

    try {
        await runSh(WS, "task.sh");
        assert.fail("EF_INFRA_IGN_EXPECT_FAIL: expected exit 10");
    } catch (err) {
        assert.equal(err.code, 10, "EF_INFRA_IGN_EXIT10: expected exit code 10");
        assert.match(String(err.stderr || ""), /MISSING_TOOLS/, "EF_INFRA_IGN_STDERR: expected MISSING_TOOLS");
    }

    const out = norm(readText(WS, "outputs/preflight.txt"));
    assert.equal(out, "STATUS=FAIL\nMISSING=git", "EF_INFRA_IGN_FILE: expected FAIL + missing git");
});

