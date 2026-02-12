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

test("stages only intended files and commits with correct message", async () => {
    sh();

    const repo = path.join(WS, "sandbox", "repo");
    assert.equal(git(repo, ["branch", "--show-current"]).trim(), "main");

    const msg = git(repo, ["log", "-1", "--pretty=%s"]).trim();
    assert.equal(msg, "Add greeting and config");

    // temp.log should be ignored (present but not tracked)
    const tracked = git(repo, ["ls-files"]).trim().split("\n").filter(Boolean).sort();
    assert.deepEqual(tracked, ["config.json", "greeting.txt"]);

    const status = git(repo, ["status", "--porcelain"]).trim();
    assert.equal(status, ""); // clean

    const summary = JSON.parse(await fs.readFile(path.join(WS, "outputs", "summary.json"), "utf8"));
    assert.deepEqual(summary.tracked.sort(), ["config.json", "greeting.txt"]);
    assert.equal(summary.ignoredPresent, true);
    assert.equal(summary.commitMessage, "Add greeting and config");
});
