import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, textContent } from "../../../_shared/react_test_helpers.mjs";
import { App } from "../../workspace/task.mjs";

test("Renders welcome div with correct text", () => {
    const { root } = runComponent(App);
    const welcome = findByTestId(root, "welcome");

    assert.equal(welcome.type, "div");
    assert.equal(textContent(welcome), "Hello React");
});
