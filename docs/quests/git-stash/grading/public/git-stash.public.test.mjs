import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const WS = process.env.EF_WORKSPACE_OVERRIDE || fileURLToPath(new URL("../../starter/", import.meta.url));
const BASH = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "bash";

const sh = () => execFileSync(BASH, ["task.sh"], { cwd: WS, encoding: "utf8" });

test.beforeEach(async () => {
    await fs.rm(path.join(WS, "outputs"), { recursive: true, force: true });
    await fs.rm(path.join(WS, "sandbox"), { recursive: true, force: true });
});

test("stashes changes cleanly then restores them", async () => {
    sh();

    const clean = (await fs.readFile(path.join(WS, "outputs", "status_clean.txt"), "utf8")).trim();
    assert.equal(clean, "");

    const dirty = (await fs.readFile(path.join(WS, "outputs", "status_dirty.txt"), "utf8")).trim();
    assert.notEqual(dirty, "");
    assert.match(dirty, /notes\.txt/);

    const stashList = await fs.readFile(path.join(WS, "outputs", "stash_list.txt"), "utf8");
    assert.match(stashList, /wip/);
});
