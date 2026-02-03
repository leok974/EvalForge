import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

async function run(env) {
    return execFileAsync(process.execPath, ["check_env.js"], { cwd: WS, env: { ...process.env, ...env }, timeout: 5000 });
}

test("defaults MODE/PORT and fails when API_KEY missing", async () => {
    try {
        await run({ MODE: "", PORT: "", API_KEY: "" });
        assert.fail("EF_INFRA_ENV_EXPECT_FAIL: expected exit 3");
    } catch (err) {
        assert.equal(err.code, 3, "EF_INFRA_ENV_EXIT3: must exit 3 when API_KEY missing");
        const out = String(err.stdout || "");
        assert.match(out, /^MODE=dev/m, "EF_INFRA_ENV_MODE_DEFAULT: MODE must default to dev");
        assert.match(out, /^PORT=3000/m, "EF_INFRA_ENV_PORT_DEFAULT: PORT must default to 3000");
        assert.match(out, /^API_KEY=MISSING/m, "EF_INFRA_ENV_KEY_MISSING: must print API_KEY=MISSING");
    }
});

test("prints SET when API_KEY present", async () => {
    const { stdout } = await run({ MODE: "prod", PORT: "8080", API_KEY: "xyz" });
    assert.match(stdout, /^MODE=prod/m, "EF_INFRA_ENV_MODE_SET");
    assert.match(stdout, /^PORT=8080/m, "EF_INFRA_ENV_PORT_SET");
    assert.match(stdout, /^API_KEY=SET/m, "EF_INFRA_ENV_KEY_SET");
});
