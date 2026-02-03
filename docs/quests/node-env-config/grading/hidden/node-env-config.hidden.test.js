import test from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const WS = fileURLToPath(new URL("../../starter/", import.meta.url));

test("Fails if DB_URL is missing", async () => {
    const envNoDb = { ...process.env };
    delete envNoDb.DB_URL;
    delete envNoDb.PORT;

    try {
        await execFileAsync(process.execPath, ["index.js"], {
            cwd: WS,
            env: envNoDb,
            shell: false
        });
    } catch (err) {
        assert.notEqual(err.code, 0, "EF_ENV_DB_URL_REQUIRED_EXIT: Exit code should be non-zero");
        return;
    }
    assert.fail("EF_ENV_DB_URL_REQUIRED: Should exit non-zero if DB_URL is missing");
});
