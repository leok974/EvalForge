import test from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const starterDir = fileURLToPath(new URL("../../starter", import.meta.url));

test("npm start works and listens on env PORT", async () => {
    // We'll try running the start script with a custom port
    const controller = new AbortController();
    const { signal } = controller;

    // We can't use execFile for "npm start" easily on windows without shell:true, 
    // or calling npm directly. 
    // Let's use `npm start` via shell execution, but kill it quickly.

    // Alternatively, verify package.json has "start" and run app.js directly?
    // The quest requirement says "Add start script".
    // Let's check package.json first.

    // Check start script existence
    // But let's implicitly check it by running it.

    const child = execFile("npm", ["run", "start"], {
        cwd: starterDir,
        env: { ...process.env, PORT: "5555" },
        shell: true // needed for npm on windows often
    });

    // Wait for stdout 'Server listening on port 5555'
    await new Promise((resolve, reject) => {
        let output = "";
        child.stdout.on("data", (chunk) => {
            output += chunk;
            if (output.includes("Server listening on port 5555")) {
                resolve();
                child.kill();
            }
        });

        child.stderr.on("data", (chunk) => output += chunk);

        child.on("error", reject);
        child.on("exit", (code) => {
            if (code !== 0 && !child.killed) {
                reject(new Error("App exited prematurely: " + output));
            }
        });

        // Timeout
        setTimeout(() => {
            child.kill();
            reject(new Error("Timeout waiting for server start. Output: " + output));
        }, 3000);
    });

    assert.ok(true, "EF_DEPLOY_START: npm start should run and respect PORT");
});
