import test from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const WS = fileURLToPath(new URL("../../workspace/", import.meta.url));

async function run(cmd, args) {
    return execFileAsync(cmd, args, { cwd: WS, shell: true });
}

test("npm test passes", async () => {
    await run("npm", ["test"]);
});

test("npm run start prints OK", async () => {
    const { stdout } = await run("npm", ["run", "start"]);
    assert.match(stdout, /OK/, "EF_NODE_NPM_START_OK");
});

test("npm run check-lockfile passes", async () => {
    const { stdout } = await run("npm", ["run", "check-lockfile"]);
    assert.match(stdout, /Lockfile OK/i, "EF_NODE_NPM_LOCKFILE_OK");
});
