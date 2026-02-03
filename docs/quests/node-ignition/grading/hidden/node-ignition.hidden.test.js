import test from "node:test";
import assert from "node:assert/strict";
import { greet } from "../../starter/src/greet.js";

test("greet() trims whitespace", () => {
    assert.equal(
        greet("  Leo  "),
        "Hello, Leo!",
        "EF_NODE_IGNITION_TRIM: greet should trim whitespace"
    );
});

test("greet() rejects empty after trim", () => {
    assert.throws(
        () => greet("   "),
        /empty|name|blank|invalid|EF_/i,
        "EF_NODE_IGNITION_EMPTY: greet should throw on empty/whitespace-only"
    );
});
