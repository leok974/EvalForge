import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");

test("does not bind only to 127.0.0.1", () => {
    const s = fs.readFileSync(path.join(WS, "server.js"), "utf8");
    assert.ok(!/127\.0\.0\.1/.test(s), "EF_INFRA_PORTS_NO_LOOPBACK: must not bind to 127.0.0.1");
    assert.match(s, /0\.0\.0\.0/, "EF_INFRA_PORTS_BIND_ALL: must bind to 0.0.0.0");
});
