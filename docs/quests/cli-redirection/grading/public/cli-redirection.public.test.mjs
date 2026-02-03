import test from "node:test";
import assert from "node:assert/strict";
import { workspaceDirFromTestFile, runSh, readTextTrim } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("report contains header + data + footer", async () => {
    await runSh({ ws: WS });
    // readTextTrim handles CRLF normalization
    const lines = readTextTrim(WS, "outputs/report.txt").split("\n");
    assert.equal(lines[0], "HEADER", "EF_CLI_REDIRECT_HEADER: first line must be HEADER");
    assert.equal(lines.at(-1), "FOOTER", "EF_CLI_REDIRECT_FOOTER: last line must be FOOTER");
    assert.equal(lines.slice(1, -1).join("\n"), readTextTrim(WS, "fixtures/data.txt"), "EF_CLI_REDIRECT_BODY: middle must match fixtures/data.txt");
});
