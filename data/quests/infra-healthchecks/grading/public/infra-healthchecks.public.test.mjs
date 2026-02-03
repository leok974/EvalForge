import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawn } from "node:child_process";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

async function startServer() {
    const proc = spawn(process.execPath, ["server.js"], { cwd: WS, env: { ...process.env, PORT: "0" }, stdio: ["ignore", "pipe", "pipe"] });
    let buf = "";
    const port = await new Promise((resolve, reject) => {
        const t = setTimeout(() => reject(new Error("timeout waiting PORT")), 3000);
        proc.stdout.on("data", (d) => {
            buf += d.toString("utf8");
            const m = buf.match(/PORT\s+(\d+)/);
            if (m) { clearTimeout(t); resolve(Number(m[1])); }
        });
        proc.on("exit", (c) => reject(new Error(`server exited ${c}: ${buf}`)));
    });
    return { proc, port };
}

test("/health returns 200 ok; /ready returns 503 when flag missing", async () => {
    const { proc, port } = await startServer();
    try {
        const h = await fetch(`http://127.0.0.1:${port}/health`);
        assert.equal(h.status, 200, "EF_INFRA_HC_HEALTH_200");
        assert.equal(await h.text(), "ok", "EF_INFRA_HC_HEALTH_BODY");

        const r = await fetch(`http://127.0.0.1:${port}/ready`);
        assert.equal(r.status, 503, "EF_INFRA_HC_READY_503");
    } finally {
        proc.kill();
    }
});
