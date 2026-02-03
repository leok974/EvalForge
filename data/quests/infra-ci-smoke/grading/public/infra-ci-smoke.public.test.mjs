import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("ci includes checkout, setup-node, npm ci, npm test", () => {
    const s = fs.readFileSync(path.join(WS, "ci.yml"), "utf8");
    assert.match(s, /actions\/checkout@/m, "EF_INFRA_CI_CHECKOUT: must include actions/checkout");
    assert.match(s, /actions\/setup-node@/m, "EF_INFRA_CI_SETUP_NODE: must include actions/setup-node");
    assert.match(s, /\bnpm ci\b/m, "EF_INFRA_CI_NPM_CI: must run npm ci");
    assert.match(s, /\bnpm test\b/m, "EF_INFRA_CI_NPM_TEST: must run npm test");
});
