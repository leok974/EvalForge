import test from "node:test";
import assert from "node:assert/strict";
import { workspaceDirFromTestFile, runSh, readTextTrim, exists } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("report contains header + data + footer", async () => {
    const { status, stdout, stderr } = await runSh({ ws: WS });

    assert.equal(status, 0, "EF_CLI_REDIRECT_EXIT_0: must exit 0");
    assert.equal((stdout ?? "").trim(), "", "EF_CLI_REDIRECT_STDOUT_EMPTY: no stdout");
    assert.equal((stderr ?? "").trim(), "", "EF_CLI_REDIRECT_STDERR_EMPTY: no stderr");

    assert.ok(exists(WS, "outputs/report.txt"), "EF_CLI_REDIRECT_REPORT_EXISTS: outputs/report.txt must exist");

    // readTextTrim handles CRLF normalization
    const lines = readTextTrim(WS, "outputs/report.txt").split("\n");
    assert.equal(lines[0], "HEADER", "EF_CLI_REDIRECT_HEADER: first line must be HEADER");
    assert.equal(lines.at(-1), "FOOTER", "EF_CLI_REDIRECT_FOOTER: last line must be FOOTER");

    const expectedBody = readTextTrim(WS, "fixtures/data.txt");
    const actualBody = lines.slice(1, -1).join("\n");
    assert.equal(actualBody, expectedBody, "EF_CLI_REDIRECT_BODY: middle must match fixtures/data.txt");
});
