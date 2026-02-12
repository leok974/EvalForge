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

test("creates annotated tag v1.0.0 pointing to HEAD", async () => {
    sh();

    const repo = path.join(WS, "sandbox", "repo");
    const tagType = (await fs.readFile(path.join(WS, "outputs", "tag_type.txt"), "utf8")).trim();
    assert.equal(tagType, "tag");

    const target = (await fs.readFile(path.join(WS, "outputs", "tag_target.txt"), "utf8")).trim();
    const head = git(repo, ["rev-parse", "HEAD"]).trim();
    assert.equal(target, head);
});
