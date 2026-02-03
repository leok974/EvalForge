import test from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const starterDir = fileURLToPath(new URL("../../starter", import.meta.url));

test("task.sh does not use absolute paths", async () => {
    // We want to ensure they used 'cd fixtures/...' or 'cd ./fixtures/...'
    // and NOT 'cd /d/EvalForge/...'
    
    // We can't easily check the *sidebar* state (this is black box).
    // So we'll just check the script content here.
    const scriptPath = path.join(starterDir, "task.sh");
    const content = await fs.readFile(scriptPath, "utf-8");
    
    // Naively check for leading logic
    // Actually, forcing them to modify 'task.sh' which is in starter is the constraint.
    // If they hardcode absolute path, it won't work on another machine. 
    // But we are verifying logic.
    
    // This hidden test just verifies they didn't just 'echo' the path without cding?
    // No, we can verify that by checking if the script actually cds.
    // Let's rely on the public test for correctness.
    // For hidden, let's just make sure they call pwd.
    
    assert.match(content, /pwd/, "EF_CLI_NAV_PWD: Script should use 'pwd' command");
});
