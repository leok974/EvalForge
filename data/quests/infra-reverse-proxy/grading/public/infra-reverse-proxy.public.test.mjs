import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("extracts location -> proxy_pass in order", async () => {
    await runSh(WS, "task.sh");
    assert.equal(
        norm(readText(WS, "outputs/routes.txt")),
        "/api/ -> http://backend:8000/\n/static/ -> http://cdn:9000/\n/ -> http://frontend:5173/",
        "EF_INFRA_PROXY_ROUTES"
    );
});

