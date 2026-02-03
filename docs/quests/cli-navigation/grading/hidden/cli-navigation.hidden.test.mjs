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
const PAGES_DIR = path.join(WS, "fixtures/site/pages");

async function runTask() {
    const sh = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "sh";
    return execFileAsync(sh, ["task.sh"], { cwd: WS, timeout: 5000 });
}

test("pages.txt is dynamic (not hardcoded)", async () => {
    const extra = path.join(PAGES_DIR, "contact.html");
    fs.writeFileSync(extra, "<h1>Contact</h1>\n", "utf8");

    try {
        await runTask();
        const out = fs.readFileSync(path.join(WS, "outputs/pages.txt"), "utf8");
        assert.match(out, /contact\.html/, "EF_CLI_NAV_LIST_DYNAMIC: pages.txt must include contact.html if present");
    } finally {
        fs.unlinkSync(extra);
    }
});
