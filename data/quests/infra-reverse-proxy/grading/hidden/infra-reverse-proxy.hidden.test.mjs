import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("rejects proxy_pass without trailing slash in /api/ location", () => {
    const s = fs.readFileSync(path.join(WS, "nginx.conf"), "utf8");
    assert.ok(!/location\s+\/api\/[\s\S]*proxy_pass\s+http:\/\/api:8000;/.test(s), "EF_INFRA_NGX_NO_STRIP: api proxy_pass must end with / to strip /api/");
});
