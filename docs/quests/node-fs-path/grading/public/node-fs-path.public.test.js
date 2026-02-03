import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const starterDir = fileURLToPath(new URL("../../starter", import.meta.url));

// Ensure clean state
test.beforeEach(async () => {
    try {
        await fs.unlink(path.join(starterDir, "output.txt"));
    } catch { }
});

test("processFile creates output.txt with uppercase content", async () => {
    // Run index.js from the starter directory
    await execFileAsync(process.execPath, ["index.js"], {
        cwd: starterDir,
        shell: false
    });

    const outputPath = path.join(starterDir, "output.txt");
    const content = await fs.readFile(outputPath, "utf-8");

    assert.match(content, /HELLO WORLD/, "EF_FS_UPPERCASE: Content must be uppercase");
    assert.match(content, /NODE IS FUN/, "EF_FS_CONTENT: Content must match input");
});
