import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

function idxOfLine(re) {
    const lines = fs.readFileSync(path.join(WS, "Dockerfile"), "utf8").split("\n");
    const i = lines.findIndex((l) => re.test(l));
    assert.ok(i >= 0, `EF_INFRA_DOCKER_ORDER_MISSING: missing line for ${re}`);
    return i;
}

test("orders COPY package manifests before npm ci, and copies app after", () => {
    const iCopyPkg = idxOfLine(/^COPY\s+package(\*|\.)?json/i);
    const iNpmCi = idxOfLine(/^RUN\s+npm\s+ci/i);
    const iCopyAll = idxOfLine(/^COPY\s+\.\s+\./i);

    assert.ok(iCopyPkg < iNpmCi, "EF_INFRA_DOCKER_ORDER_PKG: COPY package*.json must come before RUN npm ci");
    assert.ok(iNpmCi < iCopyAll, "EF_INFRA_DOCKER_ORDER_APP: COPY . . must come after RUN npm ci");
});
