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

test("definitions are non-empty and not TODO", async () => {
    await execFileAsync("bash", ["task.sh"], { cwd: WS, timeout: 5000 });
    const defs = fs.readFileSync(path.join(WS, "outputs/definitions.txt"), "utf8");
    assert.ok(!/TODO/i.test(defs), "EF_INFRA_IC_NO_TODO: remove TODO placeholders");
    assert.ok(defs.split("\n").filter(l => l.trim()).every((l) => l.includes("=") && l.split("=").at(1).trim().length > 5),
        "EF_INFRA_IC_NONEMPTY: each line must have meaningful content");
});
