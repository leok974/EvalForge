import test from "node:test";
import assert from "node:assert/strict";
import { readText, mustContain, mustNotContain } from "./_h.mjs";

test("Dockerfile layers: optimize cache", () => {
    const t = readText("workspace/Dockerfile");
    mustNotContain(t, "TODO");

    const lines = t.split("\n").map(l => l.trim()).filter(l => l && !l.startsWith("#"));
    
    // Find indices
    const idxCopyPkg = lines.findIndex(l => l.match(/COPY\s+package.*json/));
    const idxRunNpm = lines.findIndex(l => l.match(/RUN\s+npm\s+ci/));
    const idxCopyAll = lines.findIndex(l => l === "COPY . .");

    assert.ok(idxCopyPkg !== -1, "Missing COPY package*.json");
    assert.ok(idxRunNpm !== -1, "Missing RUN npm ci");
    assert.ok(idxCopyAll !== -1, "Missing COPY . .");

    assert.ok(idxCopyPkg < idxRunNpm, "COPY package.json must be before RUN npm ci");
    assert.ok(idxRunNpm < idxCopyAll, "RUN npm ci must be before COPY . .");
});
