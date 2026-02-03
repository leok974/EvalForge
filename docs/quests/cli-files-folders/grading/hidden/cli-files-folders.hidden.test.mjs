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

test("copy is real (not hardcoded) and fixtures remain", async () => {
    const invoicePath = path.join(WS, "fixtures/invoice.txt");
    const original = fs.readFileSync(invoicePath, "utf8");

    // mutate fixture to ensure script copies from file (not hardcoded content)
    fs.writeFileSync(invoicePath, "INVOICE_ID=XYZ-999\nTOTAL=123.45\n", "utf8");

    try {
        await runTask();

        const archived = fs.readFileSync(path.join(WS, "sandbox/archive/2026/invoice.txt"), "utf8");
        assert.match(archived, /XYZ-999/, "EF_CLI_FF_DYNAMIC_COPY: archived invoice must reflect fixtures/invoice.txt");

        // Ensure fixtures still exist after run
        assert.ok(fs.existsSync(invoicePath), "EF_CLI_FF_FIXTURES_EXIST: fixtures must not be deleted");
        // As noted in public test: if solution moves readme, this will fail.
        assert.ok(fs.existsSync(path.join(WS, "fixtures/readme.md")), "EF_CLI_FF_FIXTURES_EXIST2: fixtures/readme.md must remain");
    } finally {
        // restore
        fs.writeFileSync(invoicePath, original, "utf8");
    }
});
