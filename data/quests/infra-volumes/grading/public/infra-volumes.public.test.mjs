import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("mounts named volume pg_data to postgres data directory", () => {
    const s = fs.readFileSync(path.join(WS, "docker-compose.yml"), "utf8");
    assert.match(s, /volumes:\s*\n\s*-\s*pg_data:\/var\/lib\/postgresql\/data/m, "EF_INFRA_VOL_MOUNT: must mount pg_data");
});
