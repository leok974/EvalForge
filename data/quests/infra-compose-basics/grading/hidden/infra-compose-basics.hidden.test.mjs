import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("uses named volume db_data for postgres persistence and avoids localhost", () => {
    const s = fs.readFileSync(path.join(WS, "docker-compose.yml"), "utf8");
    assert.match(s, /volumes:\s*\n([\s\S]*?)db_data:/m, "EF_INFRA_COMP_VOL_DEF: must define top-level db_data volume");
    assert.match(s, /db_data:\s*\/var\/lib\/postgresql\/data/m, "EF_INFRA_COMP_VOL_MOUNT: must mount db_data to postgres data dir");
    assert.ok(!/localhost/i.test(s), "EF_INFRA_COMP_NO_LOCALHOST: must not reference localhost in compose networking");
});
