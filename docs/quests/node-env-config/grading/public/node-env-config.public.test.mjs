import test from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const WS = fileURLToPath(new URL("../../workspace/", import.meta.url));

async function run(env) {
    return execFileAsync(process.execPath, ["index.js"], {
        cwd: WS,
        env: { ...process.env, ...env },
        shell: false
    });
}

test("Uses PORT from env", async () => {
    const { stdout } = await run({ PORT: "5000", DB_URL: "mysql://localhost" });
    assert.match(stdout, /Server starting on port 5000/, "EF_ENV_PORT_READ");
});

test("Defaults PORT to 3000 if missing", async () => {
    const envNoPort = { ...process.env, DB_URL: "mysql://localhost" };
    delete envNoPort.PORT;

    const { stdout } = await execFileAsync(process.execPath, ["index.js"], {
        cwd: WS,
        env: envNoPort,
        shell: false
    });

    assert.match(stdout, /Server starting on port 3000/, "EF_ENV_PORT_DEFAULT");
});

test("Fails if DB_URL is missing", async () => {
    const envNoDb = { ...process.env };
    delete envNoDb.DB_URL;

    const res = await execFileAsync(process.execPath, ["index.js"], {
        cwd: WS,
        env: envNoDb,
        shell: false
    }).then(
        () => ({ ok: true }),
        (err) => ({ ok: false, err })
    );

    assert.equal(res.ok, false, "EF_ENV_DB_URL_MUST_FAIL");
    // The failure can appear in stderr or in the thrown error message depending on Node.
    const msg = res.err ? String(res.err.stderr || res.err.message || "") : "";
    assert.match(msg, /DB_URL/i, "EF_ENV_DB_URL_REQUIRED");
});
