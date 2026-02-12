import test from "node:test";
import assert from "node:assert/strict";
import { requestLogger, authMiddleware, errorMiddleware } from "../../workspace/middleware.js";

test("requestLogger logs method + url and calls next", (t, done) => {
    const logs = [];
    const orig = console.log;
    console.log = (msg) => logs.push(String(msg));

    const req = { method: "GET", url: "/" };
    const res = {};
    const next = () => {
        try {
            assert.deepEqual(logs, ["GET /"], "EF_NODE_MW_LOG_FORMAT");
            done();
        } finally {
            console.log = orig;
        }
    };

    requestLogger(req, res, next);
});

test("authMiddleware accepts correct key and calls next", (t, done) => {
    const req = { headers: { "x-api-key": "secret123" } };
    const res = {};
    const next = () => done();
    authMiddleware(req, res, next);
});

test("authMiddleware rejects incorrect key (401 + Unauthorized) and does NOT call next", (t, done) => {
    const req = { headers: { "x-api-key": "wrong" } };

    const res = {
        statusCode: 200,
        ended: false,
        end: (msg) => {
            res.ended = true;
            assert.equal(res.statusCode, 401, "EF_NODE_MW_AUTH_STATUS");
            assert.equal(msg, "Unauthorized", "EF_NODE_MW_AUTH_MSG");
            done();
        }
    };

    const next = () => assert.fail("EF_NODE_MW_AUTH_NEXT");
    authMiddleware(req, res, next);
});

test("errorMiddleware logs error, sets 500, ends response, and does NOT call next", () => {
    const logs = [];
    const orig = console.log;
    console.log = (msg) => logs.push(String(msg));

    let nextCalled = false;
    const req = {};
    const res = {
        statusCode: 200,
        endedMsg: null,
        end: (msg) => {
            res.endedMsg = msg;
        }
    };

    try {
        errorMiddleware(new Error("Boom"), req, res, () => {
            nextCalled = true;
        });
    } finally {
        console.log = orig;
    }

    assert.deepEqual(logs, ["Boom"], "EF_NODE_MW_ERR_LOG");
    assert.equal(res.statusCode, 500, "EF_NODE_MW_ERR_500");
    assert.equal(res.endedMsg, "Internal Server Error", "EF_NODE_MW_ERR_BODY");
    assert.equal(nextCalled, false, "EF_NODE_MW_ERR_NO_NEXT");
});
