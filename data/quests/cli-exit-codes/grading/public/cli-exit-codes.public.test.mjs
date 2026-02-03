import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import {
    runSh,
    readText,
    writeText,
    withRestoredFile
} from "../../../_shared/node_test_helpers.mjs";

const WS = path.resolve(import.meta.dirname, "../../workspace");

test("prints BAD to stderr and exits 5 when FAIL present", async () => {
    await withRestoredFile(WS, "fixtures/input.txt", async () => {
        writeText(WS, "fixtures/input.txt", "OK\nFAIL\n");
        try {
            await runSh(WS);
            assert.fail("EF_CLI_EXIT_EXPECT_FAIL: expected non-zero exit");
        } catch (err) {
            assert.equal(err.code, 5, "EF_CLI_EXIT_CODE_5: expected exit code 5");
            assert.match(String(err.stderr || ""), /BAD/, "EF_CLI_EXIT_BAD: expected BAD on stderr");
        }
    });
});

test("prints OK and exits 0 when FAIL absent", async () => {
    await withRestoredFile(WS, "fixtures/input.txt", async () => {
        writeText(WS, "fixtures/input.txt", "OK\nOK\n");
        const { stdout, stderr } = await runSh(WS);
        assert.equal(stderr.trim(), "", "EF_CLI_EXIT_STDERR_EMPTY: expected no stderr on success");
        assert.equal(stdout.trim(), "OK", "EF_CLI_EXIT_OK: expected OK on stdout");
    });
});
