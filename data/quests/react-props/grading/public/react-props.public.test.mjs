import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId } from "../../../_shared/react_test_helpers.mjs";
import { Welcome } from "../../workspace/task.mjs";

test("renders prop name", () => {
    const { root } = runComponent(Welcome, { name: "Alice" });
    const h1 = findByTestId(root, "welcome");
    assert.equal(h1.children[0], "Hello, Alice!", "EF_REACT_PROPS_NAME");
});

test("renders default stranger", () => {
    const { root } = runComponent(Welcome, {});
    const h1 = findByTestId(root, "welcome");
    assert.equal(h1.children[0], "Hello, Stranger!", "EF_REACT_PROPS_DEFAULT");
});
