import test from "node:test";
import assert from "node:assert/strict";
import { pathToFileURL, fileURLToPath } from "node:url";
import path from "node:path";

const WS = fileURLToPath(new URL("../../starter/", import.meta.url));

test("math module can be imported (ESM)", async () => {
    const mathUrl = pathToFileURL(path.join(WS, "src", "math.js")).href;
    const mod = await import(mathUrl);
    assert.equal(typeof mod.mul, "function", "EF_NODE_MODULES_EXPORT: math.js must export function mul");
    assert.equal(mod.mul(3, 4), 12, "EF_NODE_MODULES_MUL: mul(3,4) should be 12");
});
