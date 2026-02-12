import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const WS = process.env.EF_WORKSPACE_OVERRIDE || fileURLToPath(new URL("../../starter/", import.meta.url));
const BASH = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "bash";
const toPosix = (p) => p.split(path.sep).join("/");

const sh = () => execFileSync(BASH, ["task.sh"], { cwd: WS, encoding: "utf8" });
const git = (cwd, args) => {
    const posixCwd = toPosix(cwd);
    const argStr = args.map(a => `"${a}"`).join(" ");
    const cmd = `git -C "${posixCwd}" ${argStr}`;
    return execFileSync(BASH, ["-c", cmd], { encoding: "utf8" });
};

test.beforeEach(async () => {
    await fs.rm(path.join(WS, "outputs"), { recursive: true, force: true });
    await fs.rm(path.join(WS, "sandbox"), { recursive: true, force: true });
});

test("produces linear history (no merge commit) after rebase + ff merge", async () => {
    sh();
    const repo = path.join(WS, "sandbox", "repo");

    const parentsLine = (await fs.readFile(path.join(WS, "outputs", "parents.txt"), "utf8")).trim();
    const parts = parentsLine.split(" ").filter(Boolean);
    // linear commit => 1 parent => 2 hashes (commit + parent)
    assert.equal(parts.length, 2, "Expected HEAD to have exactly one parent (no merge commit)");

    const log = (await fs.readFile(path.join(WS, "outputs", "log.txt"), "utf8")).trim();
    assert.match(log, /feature/);
    assert.match(log, /main/);
    assert.match(log, /base/);

    // Ensure main branch is checked out
    assert.equal(git(repo, ["branch", "--show-current"]).trim(), "main");
});
