import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readTextTrim } from "../../../_shared/cli_test_utils.mjs";

const WS = fileURLToPath(new URL("../../workspace", import.meta.url));
const norm = (p) => p.replace(/\\/g, "/");

test("creates outputs files with correct navigation evidence", async () => {
    const { status, stdout, stderr } = await runSh({ ws: WS });

    assert.equal(status, 0, "EF_CLI_NAV_EXIT_0: must exit 0");
    assert.equal((stdout ?? "").trim(), "", "EF_CLI_NAV_STDOUT_EMPTY: no stdout");
    assert.equal((stderr ?? "").trim(), "", "EF_CLI_NAV_STDERR_EMPTY: no stderr");

    const loc = readTextTrim(WS, "outputs/location.txt");
    const pages = readTextTrim(WS, "outputs/pages.txt");
    const back = readTextTrim(WS, "outputs/back.txt");

    const expectedPagesDir = norm(path.join(WS, "fixtures", "site", "pages"));
    const expectedWs = norm(WS);

    assert.equal(
        norm(loc),
        expectedPagesDir,
        "EF_CLI_NAV_LOCATION: location.txt must equal absolute path to fixtures/site/pages"
    );

    // pages.txt must list filenames, one per line, and include expected names
    const lines = pages.split(/\r?\n/).filter(Boolean);
    assert.ok(lines.includes("about.html"), "EF_CLI_NAV_PAGES_ABOUT: must include about.html");
    assert.ok(lines.includes("contact.html"), "EF_CLI_NAV_PAGES_CONTACT: must include contact.html");
    assert.ok(lines.includes("index.html"), "EF_CLI_NAV_PAGES_INDEX: must include index.html");

    // Ensure they are filenames only (not paths)
    for (const line of lines) {
        // Basic check: if it contains a separator, it's likely a path
        const isPath = line.includes("/") || line.includes("\\");
        assert.equal(
            isPath,
            false,
            "EF_CLI_NAV_PAGES_FILENAMES_ONLY: pages.txt must contain filenames, not paths (detected separator)"
        );
        // Double check with basename for robustness
        assert.equal(
            line,
            path.basename(line),
            "EF_CLI_NAV_PAGES_FILENAMES_ONLY: pages.txt must contain filenames, not paths"
        );
    }

    assert.equal(
        norm(back),
        expectedWs,
        "EF_CLI_NAV_BACK: back.txt must equal the workspace absolute path"
    );
});
