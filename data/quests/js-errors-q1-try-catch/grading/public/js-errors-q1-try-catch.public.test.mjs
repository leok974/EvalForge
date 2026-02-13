import test from "node:test";
import assert from "node:assert/strict";
import { parseJson } from "../../workspace/main.js";

test("parseJson valid", () => {
    assert.deepEqual(parseJson('{"a":1}'), {a: 1});
});

test("parseJson invalid returns null", () => {
    assert.equal(parseJson('{bad:'), null);
});