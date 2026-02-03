import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("uses db service name in DATABASE_URL and defines a shared network", () => {
    const s = fs.readFileSync(path.join(WS, "docker-compose.yml"), "utf8");
    assert.match(s, /DATABASE_URL=.*@db:5432\/app/m, "EF_INFRA_NET_DB_HOST: DATABASE_URL must use db:5432");
    assert.match(s, /networks:\s*\n\s*app_net:\s*$/m, "EF_INFRA_NET_DEF: must define app_net network");
    assert.match(s, /api:\s*[\s\S]*?\n\s*networks:\s*\n\s*-\s*app_net/m, "EF_INFRA_NET_API_JOIN: api must join app_net");
    assert.match(s, /db:\s*[\s\S]*?\n\s*networks:\s*\n\s*-\s*app_net/m, "EF_INFRA_NET_DB_JOIN: db must join app_net");
});
