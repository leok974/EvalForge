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

test("merges feature into main with a merge commit", async () => {
    sh();
    const repo = path.join(WS, "sandbox", "repo");

    const msg = git(repo, ["log", "-1", "--pretty=%s"]).trim();
    assert.equal(msg, "Merge feature");

    const parentsLine = (await fs.readFile(path.join(WS, "outputs", "parents.txt"), "utf8")).trim();
    const parts = parentsLine.split(" ").filter(Boolean);
    // format: <commit> <parent1> <parent2>
    assert.ok(parts.length >= 3, "Expected a merge commit (2 parents)");

    // Files exist
    const base = await fs.readFile(path.join(repo, "base.txt"), "utf8");
    assert.match(base, /base/);
    await fs.access(path.join(repo, "feature.txt"));
    await fs.access(path.join(repo, "main.txt"));

    assert.equal(git(repo, ["branch", "--show-current"]).trim(), "main");
});
