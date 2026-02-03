import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const WS = path.resolve(__dirname, "../../starter"); // NOTE: Modified

async function runTask() {
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";
    return execFileAsync(sh, ["task.sh"], { cwd: WS, timeout: 5000 });
}

function read(p) {
    return fs.readFileSync(path.join(WS, p), "utf8").trimEnd();
}

test("creates outputs files with correct navigation evidence", async () => {
    await runTask();

    const loc = read("outputs/location.txt");
    const back = read("outputs/back.txt");
    const pages = read("outputs/pages.txt").split("\n").filter(Boolean);

    // NOTE: Normalized expected paths for 'starter' naming
    assert.match(
        loc,
        /\/starter\/fixtures\/site\/pages$/,
        "EF_CLI_NAV_LOCATION: location.txt must end with /starter/fixtures/site/pages"
    );
    assert.match(
        back,
        /\/starter$/,
        "EF_CLI_NAV_BACK: back.txt must end with /starter"
    );

    assert.ok(pages.includes("index.html"), "EF_CLI_NAV_LIST_INDEX: pages.txt must include index.html");
    assert.ok(pages.includes("about.html"), "EF_CLI_NAV_LIST_ABOUT: pages.txt must include about.html");
});
