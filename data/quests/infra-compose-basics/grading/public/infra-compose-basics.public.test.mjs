import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const yml = () => fs.readFileSync(path.join(WS, "docker-compose.yml"), "utf8");

test("compose defines api + db and correct postgres image", () => {
    const s = yml();
    assert.match(s, /services:\s*/m, "EF_INFRA_COMP_SERVICES: missing services:");
    assert.match(s, /^\s*api:\s*$/m, "EF_INFRA_COMP_API: missing api service");
    assert.match(s, /^\s*db:\s*$/m, "EF_INFRA_COMP_DB: missing db service");
    assert.match(s, /image:\s*postgres:16-alpine/m, "EF_INFRA_COMP_PG_IMAGE: db must use postgres:16-alpine");
});

test("api depends_on db and uses db hostname in DATABASE_URL", () => {
    const s = yml();
    assert.match(s, /depends_on:\s*\n\s*-\s*db/m, "EF_INFRA_COMP_DEPENDS: api must depend_on db");
    assert.match(s, /DATABASE_URL=.*db:5432/m, "EF_INFRA_COMP_DB_HOST: DATABASE_URL must use db:5432");
});
