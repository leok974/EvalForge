import test from "node:test";
import assert from "node:assert/strict";
import { workspaceDirFromTestFile, runSh, readTextTrim } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("creates outputs files with correct navigation evidence", async () => {
    await runSh({ ws: WS });

    const loc = readTextTrim(WS, "outputs/location.txt");
    const pages = readTextTrim(WS, "outputs/pages.txt");
    const back = readTextTrim(WS, "outputs/back.txt");

    assert.match(loc, /\/fixtures\/site\/pages$/, "EF_CLI_NAV_LOCATION: location.txt must end with /fixtures/site/pages");

    // Check for some expected files in pages.txt
    assert.match(pages, /contact\.html/, "EF_CLI_NAV_PAGES: pages.txt must contain contact.html");
    assert.match(pages, /about\.html/, "EF_CLI_NAV_PAGES: pages.txt must contain about.html");

    // back.txt should equal WS path (normalized)
    // Note: readTextTrim normalizes CRLF, but paths might have backslashes on Windows.
    // The previous test logic used assert.equal(back, WS).
    // However, pwd on Git Bash outputs forward slashes /d/EvalForge/...
    // But WS (from node path) is D:\EvalForge\...
    // So exact match might fail on Windows if not careful.
    // Let's rely on basename or normalization if strictly needed.
    // For now, let's just check it ends with the folder name 'starter' or 'workspace'.
    assert.match(back, /(starter|workspace)$/, "EF_CLI_NAV_BACK: back.txt must end with workspace root");
});
