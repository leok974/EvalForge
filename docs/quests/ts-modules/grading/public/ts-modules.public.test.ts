import test from "node:test";
import assert from "node:assert/strict";

import { sum, toCents } from "../../workspace/math.ts";
import { formatInvoiceTotal } from "../../workspace/task.ts";

test("math.sum sums numbers and handles empty array", () => {
    assert.equal(sum([]), 0, "EF_TS_MOD_SUM_EMPTY");
    assert.equal(sum([1, 2, 3]), 6, "EF_TS_MOD_SUM_BASIC");
});

test("math.toCents converts dollars to cents with rounding", () => {
    assert.equal(toCents(0), 0, "EF_TS_MOD_CENTS_0");
    assert.equal(toCents(1.23), 123, "EF_TS_MOD_CENTS_123");
    assert.equal(toCents(1.005), 101, "EF_TS_MOD_CENTS_ROUND"); // rounding check
});

test("formatInvoiceTotal computes total cents deterministically", () => {
    const out = formatInvoiceTotal([10, 32.5]);
    assert.equal(out, "Total: 4250 cents", "EF_TS_MOD_TOTAL");
});

test("formatInvoiceTotal handles empty invoice", () => {
    const out = formatInvoiceTotal([]);
    assert.equal(out, "Total: 0 cents", "EF_TS_MOD_EMPTY");
});
