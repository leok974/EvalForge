import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { workspaceDirFromTestFile, runSh, exists, readTextTrim, withRestoredFile } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("copy is real (not hardcoded) and fixtures remain", async () => {
    // "cp fixtures/invoice.txt -> sandbox/archive/2026/invoice.txt"
    // This preserves original invoice.txt
    await runSh({ ws: WS });
    assert.ok(exists(WS, "fixtures/invoice.txt"), "EF_CLI_FF_INVOICE_PRESERVED: fixtures/invoice.txt must remain");
});

test("dynamic: handles changed invoice content", async () => {
    await withRestoredFile(WS, "fixtures/invoice.txt", async () => {
        fs.writeFileSync(path.join(WS, "fixtures/invoice.txt"), "NEW_CONTENT");
        await runSh({ ws: WS });
        const content = readTextTrim(WS, "sandbox/archive/2026/invoice.txt");
        assert.equal(content, "NEW_CONTENT", "EF_CLI_FF_DYNAMIC: copied content matches source");
    });
});
