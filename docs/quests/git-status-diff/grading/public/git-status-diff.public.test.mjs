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

test("writes porcelain + diffstat matching expected changes", async () => {
    sh();

    const repo = path.join(WS, "sandbox", "repo");

    const porcelain = await fs.readFile(path.join(WS, "outputs", "porcelain.txt"), "utf8");
    // M app.txt, ?? notes.md
    assert.match(porcelain, /^ M app\.txt/m);
    assert.match(porcelain, /^\?\? notes\.md/m);

    const diffstat = await fs.readFile(path.join(WS, "outputs", "diffstat.txt"), "utf8");
    assert.match(diffstat, /app\.txt/);

    // Ensure repo has exactly 1 commit, changes uncommitted
    assert.equal(git(repo, ["rev-list", "--count", "HEAD"]).trim(), "1");
    assert.notEqual(git(repo, ["status", "--porcelain"]).trim(), "");
});
