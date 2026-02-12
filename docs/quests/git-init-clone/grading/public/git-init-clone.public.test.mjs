import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const WS = process.env.EF_WORKSPACE_OVERRIDE || fileURLToPath(new URL("../../starter/", import.meta.url));

// Use Git Bash explicitly on Windows to avoid WSL bash
const BASH = process.platform === "win32" ? "C:\\Program Files\\Git\\bin\\bash.exe" : "bash";
const toPosix = (p) => p.split(path.sep).join("/");

const sh = (args, opts = {}) =>
    execFileSync(BASH, args, { cwd: WS, encoding: "utf8", ...opts });

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

test("creates repo, bare remote, clone, and report.json", async () => {
    sh(["task.sh"]);

    const reportPath = path.join(WS, "outputs", "report.json");
    const report = JSON.parse(await fs.readFile(reportPath, "utf8"));

    assert.equal(report.repoExists, true);
    assert.equal(report.branch, "main");
    assert.equal(report.commitCount, 1);
    assert.equal(report.headMessage, "init");
    assert.equal(report.cloneHasGit, true);

    const repoDir = path.join(WS, "sandbox", "repo");
    const cloneDir = path.join(WS, "sandbox", "clone");
    const remoteDir = path.join(WS, "sandbox", "remote.git");

    // Repo sanity
    assert.match(git(repoDir, ["rev-parse", "--is-inside-work-tree"]).trim(), /^true$/);
    assert.match(git(repoDir, ["branch", "--show-current"]).trim(), /^main$/);

    // Commit sanity
    const msg = git(repoDir, ["log", "-1", "--pretty=%s"]).trim();
    assert.equal(msg, "init");

    // Bare remote has refs
    const refs = git(remoteDir, ["show-ref"]).trim();
    assert.match(refs, /refs\/heads\/main/);

    // Clone has git + file
    assert.match(git(cloneDir, ["rev-parse", "--is-inside-work-tree"]).trim(), /^true$/);
    const hello = await fs.readFile(path.join(cloneDir, "hello.txt"), "utf8");
    assert.match(hello, /hello/);
});
