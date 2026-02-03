import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { workspaceDirFromTestFile, runSh, exists, readTextTrim } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("creates required structure and preserves fixtures", async () => {
    // Ensure clean state handled by task.sh (it removes sandbox/tmp usually? No, the goal is to make changes)
    // The previous starter task.sh didn't clean up, but the solution does.
    // We just run it.
    await runSh({ ws: WS });

    // Check archive invoice
    const invoicePath = "sandbox/archive/2026/invoice.txt";
    assert.ok(exists(WS, invoicePath), "EF_CLI_FF_INVOICE_EXISTS: archive invoice must exist");
    const content = readTextTrim(WS, invoicePath);
    assert.match(content, /INVOICE_ID=123/, "EF_CLI_FF_INVOICE_CONTENT: invoice content preserved");

    // Check README move (wait, task uses cp, so fixture preserved)
    assert.ok(exists(WS, "sandbox/README.md"), "EF_CLI_FF_README_EXISTS: sandbox/README.md must exist");
    assert.ok(exists(WS, "fixtures/readme.md"), "EF_CLI_FF_README_PRESERVED: fixtures/readme.md should exist");

});
