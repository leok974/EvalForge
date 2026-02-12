import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, textContent } from "../../../_shared/react_test_helpers.mjs";
import { Welcome } from "../../workspace/task.mjs";

test("With prop name='Alice': renders Hello, Alice!", () => {
    const { root } = runComponent(Welcome, { name: "Alice" });
    const h1 = findByTestId(root, "welcome");
    assert.equal(textContent(h1), "Hello, Alice!");
});

test("Without prop: renders Hello, Stranger!", () => {
    const { root } = runComponent(Welcome);
    const h1 = findByTestId(root, "welcome");
    assert.equal(textContent(h1), "Hello, Stranger!");
});
