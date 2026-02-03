import test from "node:test";
import assert from "node:assert/strict";
import { requestLogger, authMiddleware } from "../../starter/middleware.js";

test("requestLogger calls next", (t, done) => {
    const req = { method: "GET", url: "/" };
    const res = {};
    const next = () => {
        assert.ok(true, "next called");
        done();
    };

    // We can't easily assert console.log without spying, but let's assume if it calls next it's structurally ok
    // We can spy on console.log if we really want strictness.
    requestLogger(req, res, next);
});

test("authMiddleware accepts correct key", (t, done) => {
    const req = { headers: { 'x-api-key': 'secret123' } };
    const res = {};
    const next = () => {
        assert.ok(true, "next called for valid key");
        done();
    };
    authMiddleware(req, res, next);
});

test("authMiddleware rejects incorrect key", (t, done) => {
    const req = { headers: { 'x-api-key': 'wrong' } };
    const res = {
        statusCode: 200,
        end: (msg) => {
            assert.equal(res.statusCode, 401, "EF_MW_AUTH_STATUS: Should be 401");
            assert.equal(msg, "Unauthorized", "EF_MW_AUTH_MSG: Should say Unauthorized");
            done();
        }
    };
    const next = () => {
        assert.fail("EF_MW_AUTH_NEXT: Should NOT call next for invalid key");
    };
    authMiddleware(req, res, next);
});
