import test from "node:test";
import assert from "node:assert/strict";

import { classifyStatus } from "../../workspace/task.ts";

test("classifies success codes", () => {
    assert.equal(classifyStatus(200), "success", "EF_TS_CONTROL_200");
    assert.equal(classifyStatus(204), "success", "EF_TS_CONTROL_204");
    assert.equal(classifyStatus(299), "success", "EF_TS_CONTROL_299");
});

test("classifies redirect codes", () => {
    assert.equal(classifyStatus(301), "redirect", "EF_TS_CONTROL_301");
    assert.equal(classifyStatus(399), "redirect", "EF_TS_CONTROL_399");
});

test("classifies client errors", () => {
    assert.equal(classifyStatus(400), "client_error", "EF_TS_CONTROL_400");
    assert.equal(classifyStatus(418), "client_error", "EF_TS_CONTROL_418");
    assert.equal(classifyStatus(499), "client_error", "EF_TS_CONTROL_499");
});

test("classifies server errors", () => {
    assert.equal(classifyStatus(500), "server_error", "EF_TS_CONTROL_500");
    assert.equal(classifyStatus(503), "server_error", "EF_TS_CONTROL_503");
    assert.equal(classifyStatus(599), "server_error", "EF_TS_CONTROL_599");
});

test("returns invalid for non-number / non-integer / out-of-range", () => {
    assert.equal(classifyStatus("200"), "invalid", "EF_TS_CONTROL_STR");
    assert.equal(classifyStatus(null), "invalid", "EF_TS_CONTROL_NULL");
    assert.equal(classifyStatus(undefined), "invalid", "EF_TS_CONTROL_UNDEF");
    assert.equal(classifyStatus(200.5), "invalid", "EF_TS_CONTROL_FLOAT");
    assert.equal(classifyStatus(99), "invalid", "EF_TS_CONTROL_LOW");
    assert.equal(classifyStatus(600), "invalid", "EF_TS_CONTROL_HIGH");
});

test("returns invalid for 1xx (not classified in this quest)", () => {
    assert.equal(classifyStatus(100), "invalid", "EF_TS_CONTROL_100");
    assert.equal(classifyStatus(199), "invalid", "EF_TS_CONTROL_199");
});
