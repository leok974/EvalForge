import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import fs from "node:fs";
import { workspaceDirFromTestFile, runSh, readTextTrim, withRestoredFile } from "../../../_shared/cli_test_utils.mjs";

const WS = workspaceDirFromTestFile(import.meta.url);

test("pages.txt is dynamic (not hardcoded)", async () => {
    await withRestoredFile(WS, "fixtures/site/pages/new.html", async () => {
        fs.writeFileSync(path.join(WS, "fixtures/site/pages/new.html"), "<h1>New</h1>");
        await runSh({ ws: WS });
        const pages = readTextTrim(WS, "outputs/pages.txt");
        assert.match(pages, /new\.html/, "EF_CLI_NAV_DYNAMIC: pages.txt must verify new file");
    });
});
