import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const starterDir = fileURLToPath(new URL("../../starter", import.meta.url));

test("processFile handles dynamic filenames", async () => {
    const testFile = "hidden_test.txt";
    const testPath = path.join(starterDir, testFile);
    await fs.writeFile(testPath, "secret message");

    // We need a way to run processFile on a DIFFERENT file than input.txt.
    // index.js hardcodes input.txt.
    // So we'll write a temporary script in starterDir that calls processFile with our arg.

    const specificTestScript = `
        import { processFile } from "./utils.js";
        await processFile("${testFile}");
    `;
    const scriptPath = path.join(starterDir, "temp_test_runner.js");
    await fs.writeFile(scriptPath, specificTestScript);

    try {
        await execFileAsync(process.execPath, ["temp_test_runner.js"], {
            cwd: starterDir,
            shell: false
        });

        const output = await fs.readFile(path.join(starterDir, "output.txt"), "utf-8");
        assert.equal(output, "SECRET MESSAGE", "EF_FS_DYNAMIC: Should handle any filename");
    } finally {
        await fs.unlink(testPath).catch(() => { });
        await fs.unlink(scriptPath).catch(() => { });
        await fs.unlink(path.join(starterDir, "output.txt")).catch(() => { });
    }
});
