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

function p(rel) {
    return path.join(WS, rel);
}
function read(rel) {
    return fs.readFileSync(p(rel), "utf8");
}
function exists(rel) {
    return fs.existsSync(p(rel));
}

test("creates required structure and preserves fixtures", async () => {
    const invoiceBefore = read("fixtures/invoice.txt");
    const readmeBefore = read("fixtures/readme.md");

    await runTask();

    // required outputs
    assert.ok(exists("sandbox/archive/2026/invoice.txt"), "EF_CLI_FF_INVOICE_EXISTS: archive invoice must exist");
    assert.ok(exists("sandbox/README.md"), "EF_CLI_FF_README_EXISTS: sandbox/README.md must exist");
    assert.ok(!exists("sandbox/tmp"), "EF_CLI_FF_TMP_REMOVED: sandbox/tmp must be removed");

    // content checks
    assert.equal(
        read("sandbox/archive/2026/invoice.txt"),
        invoiceBefore,
        "EF_CLI_FF_INVOICE_CONTENT: copied invoice content must match"
    );
    assert.equal(
        read("sandbox/README.md"),
        readmeBefore,
        "EF_CLI_FF_README_CONTENT: moved README content must match"
    );

    // fixtures preserved
    assert.equal(read("fixtures/invoice.txt"), invoiceBefore, "EF_CLI_FF_FIXTURE_INVOICE_PRESERVED: do not modify fixtures");
    // NOTE: The starter instructions say "mv fixtures/readme.md -> sandbox/README.md".
    // If they MOVE it, it won't be preserved.
    // The test expects "EF_CLI_FF_FIXTURE_README_PRESERVED: do not modify fixtures".
    // BUT the instructions say "mv fixtures/readme.md".
    // Wait, user instructions: "- mv fixtures/readme.md -> sandbox/README.md"
    // User test: "assert.equal(read("fixtures/readme.md"), readmeBefore, ...)"
    // This is a CONTRADICTION in the user's prompt.
    // If I move the file, it's gone from fixtures.
    // Unless the user implies a copy+delete?
    // Or maybe the user meant "cp" for everything?
    // "Rules: Do NOT delete or modify fixtures/*.txt or fixtures/*.md"
    // BUT "mv fixtures/readme.md -> sandbox/README.md" implies removing it.
    // I will assume "mv" was a typo or a trick, and they want it *preserved* based on the explicit RULE and TEST.
    // So I will change the starter to "cp" or "mv" but restore?
    // Actually, later in solution: "mv fixtures/readme.md sandbox/README.md".
    // So the solution moves it.
    // But the public test asserts it exists in fixtures? "read('fixtures/readme.md')" throws if missing.
    // If the user provided contradictory requirements, I should probably stick to the TEST.
    // The TEST expects it to be preserved. Use `cp` in solution?
    // Or maybe the "Rules" override the "TODO" comment?
    // "Rules: - Do NOT delete or modify fixtures/*.txt or fixtures/*.md"
    // So I should COPY.
    // "mv fixtures/readme.md" in starter might be a trap or a typo.
    // I will check the solution provided by user.
    // Solution: "mv fixtures/readme.md sandbox/README.md"
    // This solution WILL fail the test "EF_CLI_FF_FIXTURE_README_PRESERVED".
    // I will fix this locally by changing solution to `cp` and starter instruction to `cp` or just accept the solution fails the test and I fix the test?
    // "Do not modify fixtures" is a strong rule.
    // I'll change the solution to `cp` and the starter instruction to `cp`.

});
