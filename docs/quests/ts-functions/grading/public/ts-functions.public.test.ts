import test from "node:test";
import assert from "node:assert/strict";

import { totalCents } from "../../workspace/task.ts";

test("returns 0 for non-array input", () => {
    assert.equal(totalCents(null), 0, "EF_TS_FUN_NONARRAY_NULL");
    assert.equal(totalCents("x"), 0, "EF_TS_FUN_NONARRAY_STR");
    assert.equal(totalCents({}), 0, "EF_TS_FUN_NONARRAY_OBJ");
});

test("sums valid line items", () => {
    const out = totalCents([
        { sku: "A", priceCents: 250, qty: 2 },   // 500
        { sku: "B", priceCents: 199, qty: 1 },   // 199
        { sku: "C", priceCents: 0, qty: 5 }      // 0
    ]);
    assert.equal(out, 699, "EF_TS_FUN_SUM");
});

test("ignores invalid items instead of throwing", () => {
    const out = totalCents([
        { sku: "  ", priceCents: 100, qty: 1 },     // invalid sku
        { sku: "X", priceCents: -5, qty: 1 },       // invalid price
        { sku: "Y", priceCents: 100, qty: 0 },      // invalid qty
        { sku: "Z", priceCents: 100.5, qty: 1 },    // non-integer price
        { sku: "OK", priceCents: 100, qty: 2 }      // valid => 200
    ]);
    assert.equal(out, 200, "EF_TS_FUN_IGNORE_INVALID");
});

test("qty bounds: 1..99 only", () => {
    const out = totalCents([
        { sku: "OK", priceCents: 10, qty: 1 },   // 10
        { sku: "BAD", priceCents: 10, qty: 100 } // ignore
    ]);
    assert.equal(out, 10, "EF_TS_FUN_QTY_BOUNDS");
});
