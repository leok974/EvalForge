import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("nginx proxies /api/ to api:8000 with safe trailing slash and / to web", () => {
    const s = fs.readFileSync(path.join(WS, "nginx.conf"), "utf8");
    assert.match(s, /location\s+\/api\/\s*\{[\s\S]*proxy_pass\s+http:\/\/api:8000\/;/m, "EF_INFRA_NGX_API_PROXY: must proxy_pass http://api:8000/;");
    assert.match(s, /location\s+\/\s*\{[\s\S]*proxy_pass\s+http:\/\/web:5173\/;/m, "EF_INFRA_NGX_WEB_PROXY: must proxy_pass http://web:5173/;");
});
