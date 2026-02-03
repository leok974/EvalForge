import test from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const WS = fileURLToPath(new URL("../../starter/", import.meta.url));

async function run(env) {
    // Merge current env with test env, but careful not to pollute too much
    return execFileAsync(process.execPath, ["index.js"], {
        cwd: WS,
        env: { ...process.env, ...env },
        shell: false
    });
}

test("Uses PORT from env", async () => {
    const { stdout } = await run({ PORT: "5000", DB_URL: "mysql://localhost" });
    assert.match(stdout, /Server starting on port 5000/, "EF_ENV_PORT_READ: Should read PORT from env");
});

test("Defaults PORT to 3000 if missing", async () => {
    const { stdout } = await run({ PORT: "", DB_URL: "mysql://localhost" }); // Empty string or undefined
    // Note: if PORT env is set to empty string, "process.env.PORT || 3000" might handle it if programmed well,
    // but usually unset is the key. Let's pass undefined by omitting it in a cleaner way if needed.
    // execFile env replaces the WHOLE env if strictly provided? No, { ...process.env } merges.
    // To "unset" PORT, setting it to undefined works in node spawn opt? No, typically needs to be excluded.

    const envNoPort = { ...process.env, DB_URL: "mysql://localhost" };
    delete envNoPort.PORT;

    const { stdout: stdout2 } = await execFileAsync(process.execPath, ["index.js"], {
        cwd: WS,
        env: envNoPort,
        shell: false
    });

    assert.match(stdout2, /Server starting on port 3000/, "EF_ENV_PORT_DEFAULT: Should default to 3000");
});
