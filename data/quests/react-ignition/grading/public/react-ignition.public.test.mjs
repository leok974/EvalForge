import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { runComponent, findByTestId } from "../../../_shared/react_test_helpers.mjs";
import { App } from "../../workspace/task.mjs";

test("renders welcome div with correct text", () => {
    const { root } = runComponent(App);
    const welcome = findByTestId(root, "welcome");

    assert.equal(welcome.type, "div", "EF_REACT_IGN_TYPE");
    assert.equal(welcome.children[0], "Hello React", "EF_REACT_IGN_TEXT");
});
