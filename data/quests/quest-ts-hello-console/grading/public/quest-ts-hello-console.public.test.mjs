import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import path from "node:path";

// Execute the main.ts file and check output
test("Output is correct", () => {
    // We assume running from repo root or utilizing test runner env
    // But here we need to run the TS file. 
    // Best is to use 'tsx' to run workspace/main.ts
    // We can rely on relative path from this test file: ../../workspace/main.ts
    
    const wsMain = path.resolve(import.meta.dirname, "../../workspace/main.ts");
    
    // We use 'process.execPath' (node) with --import tsx? Or just 'npx tsx'?
    // Let's assume 'npx tsx' is available or use node loader.
    // Simpler: assume the runner handles environment, preventing network access etc is not our job here.
    
    const res = spawnSync("npx", ["tsx", wsMain], { encoding: "utf8", shell: true });
    
    assert.equal(res.status, 0, "Script should exit 0");
    assert.match(res.stdout, /Hello, Prism/);
});