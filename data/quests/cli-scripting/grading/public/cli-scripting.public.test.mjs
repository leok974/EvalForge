import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import {
    runSh,
    readText,
} from "../../../_shared/node_test_helpers.mjs";

const WS = path.resolve(import.meta.dirname, "../../workspace");

test("copies src to dst when args provided", async () => {
    const src = "fixtures/hello.txt";
    const dst = "outputs/copied.txt";

    await runSh(WS, "task.sh", [src, dst]);
    const out = readText(WS, dst);
    assert.equal(out.trimEnd(), "hello world", "EF_CLI_SCRIPT_COPY: expected copied contents");
});

test("prints usage and exits 2 when missing args", async () => {
    try {
        // Empty args mainly. task.sh is default. 
        // Wait, runSh defaults args to ["task.sh"]. 
        // If we want NO args beyond task.sh:
        await runSh(WS, "task.sh"); assert.fail("EF_CLI_SCRIPT_EXPECT_EXIT: expected non-zero exit");
    } catch (err) {
        assert.equal(err.code, 2, "EF_CLI_SCRIPT_EXIT_2: expected exit code 2");
        assert.match(String(err.stderr || ""), /Usage:/, "EF_CLI_SCRIPT_USAGE: expected Usage on stderr");
    }
});
