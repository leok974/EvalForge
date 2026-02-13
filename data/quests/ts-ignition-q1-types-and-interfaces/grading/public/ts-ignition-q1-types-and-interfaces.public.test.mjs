import test from "node:test";
import assert from "node:assert/strict";
import { createItem } from "../../workspace/main.ts";

test("createItem", () => {
    const i = createItem("Rock", 5);
    assert.equal(i.name, "Rock");
    assert.equal(i.weight, 5);
});