import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId } from "../../../_shared/react_test_helpers.mjs";
import { App } from "../../workspace/task.mjs";

test("only one child element", () => {
    const { root } = runComponent(App);
    const welcome = findByTestId(root, "welcome");
    assert.equal(welcome.children.length, 1, "EF_REACT_IGN_Structure");
});
