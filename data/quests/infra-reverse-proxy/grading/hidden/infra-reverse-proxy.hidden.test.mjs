import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText, writeText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("dynamic: detects added location", async () => {
    writeText(
        WS,
        "fixtures/nginx.conf",
        "server {\n  location /x/ { proxy_pass http://x:1/; }\n  location / { proxy_pass http://a:2/; }\n}\n"
    );

    await runSh(WS, "task.sh");
    assert.equal(norm(readText(WS, "outputs/routes.txt")), "/x/ -> http://x:1/\n/ -> http://a:2/", "EF_INFRA_PROXY_DYNAMIC");
});

