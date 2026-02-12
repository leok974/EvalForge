import test from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const WS = fileURLToPath(new URL("../../workspace", import.meta.url));
const npmCmd = process.platform === "win32" ? "npm.cmd" : "npm";

function waitForLine(stream, pattern, timeoutMs = 6000) {
    return new Promise((resolve, reject) => {
        const timer = setTimeout(() => reject(new Error(`timeout waiting for ${pattern}`)), timeoutMs);
        let buf = "";
        stream.on("data", (chunk) => {
            buf += chunk.toString("utf-8");
            if (pattern.test(buf)) {
                clearTimeout(timer);
                resolve(buf);
            }
        });
    });
}

test("package.json has start script and server respects PORT + /healthz", async () => {
    const PORT = "5555";

    const child = spawn(npmCmd, ["start"], {
        cwd: WS,
        env: { ...process.env, PORT },
        stdio: ["ignore", "pipe", "pipe"]
    });

    // Ensure we always clean up.
    const cleanup = () => {
        if (!child.killed) child.kill();
    };

    try {
        // Wait for the server log (must include chosen port)
        await waitForLine(child.stdout, new RegExp(`Server listening on port\\s+${PORT}`));

        // Hit /healthz
        const res = await fetch(`http://127.0.0.1:${PORT}/healthz`);
        assert.equal(res.status, 200, "EF_NODE_DEPLOY_HEALTH_STATUS");
        const text = await res.text();
        assert.equal(text, "OK", "EF_NODE_DEPLOY_HEALTH_BODY");
    } finally {
        cleanup();
    }
});
