import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runSh, readText } from "../../../_shared/node_test_helpers.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WS = path.resolve(__dirname, "../../workspace");
const norm = (s) => s.replace(/\r\n/g, "\n").trimEnd();

test("computes CORS and cookie security flags", async () => {
    await runSh(WS, "task.sh");

    assert.equal(
        norm(readText(WS, "outputs/security_report.txt")),
        "CORS_OK=true\nCREDENTIALS=true\nCOOKIE_SECURE=true\nCOOKIE_SAMESITE=Lax",
        "EF_INFRA_CORS_REPORT"
    );
});

