import test from "node:test";
import assert from "node:assert/strict";
import { authMiddleware } from "../../starter/middleware.js";

test("authMiddleware rejects missing key", (t, done) => {
    const req = { headers: {} }; // No key
    const res = {
        statusCode: 200,
        end: (msg) => {
            assert.equal(res.statusCode, 401, "EF_MW_AUTH_MISSING: Should be 401 if key missing");
            done();
        }
    };
    const next = () => {
        assert.fail("EF_MW_AUTH_MISSING_NEXT: Should NOT call next if key missing");
    };
    authMiddleware(req, res, next);
});
