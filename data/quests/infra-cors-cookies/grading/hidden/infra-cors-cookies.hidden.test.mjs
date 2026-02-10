import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText, writeText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("dynamic: mismatched origin => CORS_OK=false; missing Secure => false; SameSite None", async () => {
    writeText(WS, "fixtures/request_origin.txt", "https://a.com\n");
    writeText(
        WS,
        "fixtures/response_headers.txt",
        "Access-Control-Allow-Origin: https://b.com\n" +
        "Access-Control-Allow-Credentials: false\n" +
        "Set-Cookie: session=abc; Path=/; SameSite=None\n"
    );

    await runSh(WS, "task.sh");
    assert.equal(
        norm(readText(WS, "outputs/security_report.txt")),
        "CORS_OK=false\nCREDENTIALS=false\nCOOKIE_SECURE=false\nCOOKIE_SAMESITE=None",
        "EF_INFRA_CORS_DYNAMIC"
    );
});

