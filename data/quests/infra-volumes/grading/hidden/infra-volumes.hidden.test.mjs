import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("defines top-level pg_data volume", () => {
    const s = fs.readFileSync(path.join(WS, "docker-compose.yml"), "utf8");
    assert.match(s, /\nvolumes:\s*\n\s*pg_data:\s*$/m, "EF_INFRA_VOL_DEF: must define top-level pg_data:");
});
