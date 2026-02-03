import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const read = (rel) => fs.readFileSync(path.join(WS, rel), "utf8").trimEnd();

test("writes required infra definitions and commands", async () => {
    await execFileAsync("bash", ["task.sh"], { cwd: WS, timeout: 5000 });

    const defs = read("outputs/definitions.txt").split("\n");
    assert.equal(defs.length, 3, "EF_INFRA_IC_DEFS_LEN: expected 3 lines in definitions.txt");
    assert.match(defs[0], /^IMAGE=/, "EF_INFRA_IC_IMAGE_KEY: first line must start with IMAGE=");
    assert.match(defs[1], /^CONTAINER=/, "EF_INFRA_IC_CONTAINER_KEY: second line must start with CONTAINER=");
    assert.match(defs[2], /^BUILD_VS_RUN=/, "EF_INFRA_IC_BVR_KEY: third line must start with BUILD_VS_RUN=");

    const defsText = defs.join("\n").toLowerCase();
    assert.match(defsText, /template/, "EF_INFRA_IC_IMAGE_TEMPLATE: IMAGE must include 'template'");
    assert.match(defsText, /running/, "EF_INFRA_IC_CONTAINER_RUNNING: CONTAINER must include 'running'");
    assert.match(defsText, /build/, "EF_INFRA_IC_BVR_BUILD: BUILD_VS_RUN must include 'build'");
    assert.match(defsText, /run/, "EF_INFRA_IC_BVR_RUN: BUILD_VS_RUN must include 'run'");

    const cmds = read("outputs/commands.txt").split("\n");
    assert.equal(cmds.length, 2, "EF_INFRA_IC_CMDS_LEN: expected 2 lines in commands.txt");
    assert.match(cmds[0], /^BUILD=docker build\b/, "EF_INFRA_IC_BUILD_CMD: BUILD must start with docker build");
    assert.match(cmds[1], /^RUN=docker run\b/, "EF_INFRA_IC_RUN_CMD: RUN must start with docker run");
});
