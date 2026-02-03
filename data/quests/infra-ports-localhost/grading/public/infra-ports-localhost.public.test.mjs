import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawn } from "node:child_process";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("binds to 0.0.0.0 and logs LISTEN", async () => {
    const proc = spawn(process.execPath, ["server.js"], {
        cwd: WS,
        env: { ...process.env, PORT: "0" },
        stdio: ["ignore", "pipe", "pipe"],
    });

    let out = "";
    const done = await new Promise((resolve, reject) => {
        const t = setTimeout(() => reject(new Error("timeout")), 3000);
        proc.stdout.on("data", (d) => {
            out += d.toString("utf8");
            if (/LISTEN\s+\d+/.test(out)) {
                clearTimeout(t);
                resolve(true);
            }
        });
        proc.stderr.on("data", (d) => (out += d.toString("utf8")));
        proc.on("exit", (code) => reject(new Error(`exited ${code}: ${out}`)));
    }).finally(() => proc.kill());

    assert.ok(done, "EF_INFRA_PORTS_LOG: expected LISTEN <port> log");
});
