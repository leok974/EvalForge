import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("does not contain TODO placeholders", () => {
    const s = fs.readFileSync(path.join(WS, "ci.yml"), "utf8");
    assert.ok(!/TODO/i.test(s), "EF_INFRA_CI_NO_TODO: remove TODO placeholders");
});
