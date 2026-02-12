import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, exists, readTextTrim, workspaceDirFromTestFile } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("creates required structure and preserves fixtures", async () => {
    const { status, stdout, stderr } = await runSh({ ws: WS });

    assert.equal(status, 0, "EF_CLI_FF_EXIT_0: must exit 0");
    assert.equal((stdout ?? "").trim(), "", "EF_CLI_FF_STDOUT_EMPTY: no stdout");
    assert.equal((stderr ?? "").trim(), "", "EF_CLI_FF_STDERR_EMPTY: no stderr");

    // Required outputs
    const archiveInvoice = "sandbox/archive/2026/invoice.txt";
    assert.ok(exists(WS, archiveInvoice), "EF_CLI_FF_INVOICE_EXISTS: archive invoice must exist");
    assert.ok(exists(WS, "sandbox/README.md"), "EF_CLI_FF_README_EXISTS: sandbox/README.md must exist");
    assert.equal(exists(WS, "sandbox/tmp"), false, "EF_CLI_FF_TMP_GONE: sandbox/tmp must not exist");

    // Fixtures must remain
    assert.ok(exists(WS, "fixtures/invoice.txt"), "EF_CLI_FF_FIXTURE_INVOICE_PRESENT: fixtures/invoice.txt must still exist");
    assert.ok(exists(WS, "fixtures/readme.md"), "EF_CLI_FF_FIXTURE_README_PRESENT: fixtures/readme.md must still exist");

    // Content equality checks (copy, not move)
    const invFixture = readTextTrim(WS, "fixtures/invoice.txt");
    const invOut = readTextTrim(WS, archiveInvoice);
    assert.equal(invOut, invFixture, "EF_CLI_FF_INVOICE_SAME: invoice copy must match fixtures exactly");
    assert.match(invOut, /INVOICE_ID=123/, "EF_CLI_FF_INVOICE_ID: invoice must contain INVOICE_ID=123");

    const mdFixture = fs.readFileSync(path.join(WS, "fixtures/readme.md"), "utf8");
    const mdOut = fs.readFileSync(path.join(WS, "sandbox/README.md"), "utf8");
    assert.equal(mdOut, mdFixture, "EF_CLI_FF_README_SAME: README copy must match fixtures exactly");
});
