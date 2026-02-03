import test from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const WS = fileURLToPath(new URL("../../starter/", import.meta.url));

test("app runs and prints Result: 6", async () => {
    const { stdout, stderr } = await execFileAsync(process.execPath, ["src/app.js"], {
        cwd: WS,
        shell: false
    });

    if (stderr.trim()) console.error("STDERR:", stderr);
    assert.equal(stderr.trim(), "", "EF_NODE_MODULES_STDERR_EMPTY: app should not write to stderr");
    assert.match(stdout.trimEnd(), /^Result:\s*6$/, "EF_NODE_MODULES_OUTPUT: expected 'Result: 6'");
});

test("project is configured to run ESM", () => {
    const pkgPath = path.join(WS, "package.json");
    const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8"));
    // Accept either "type":"module" OR .mjs strategy (but this workspace uses .js, so type module is expected)
    assert.equal(
        pkg.type,
        "module",
        "EF_NODE_MODULES_ESM_REQUIRED: set package.json { \"type\": \"module\" }"
    );
});
