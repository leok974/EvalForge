import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const wsDir = fileURLToPath(new URL("../../workspace", import.meta.url));

test.beforeEach(async () => {
    try {
        await fs.unlink(path.join(wsDir, "output.txt"));
    } catch {
        // ignore
    }
});

test("processFile creates output.txt with uppercase content", async () => {
    await execFileAsync(process.execPath, ["index.js"], {
        cwd: wsDir,
        shell: false
    });

    const outputPath = path.join(wsDir, "output.txt");
    const content = await fs.readFile(outputPath, "utf-8");

    assert.match(content, /HELLO WORLD/, "EF_NODE_FS_UPPERCASE");
    assert.match(content, /NODE IS FUN/, "EF_NODE_FS_CONTENT");
});
