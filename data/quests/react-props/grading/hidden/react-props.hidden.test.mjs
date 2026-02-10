import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId } from "../../../_shared/react_test_helpers.mjs";
import { Welcome } from "../../workspace/task.mjs";

test("dynamic prop values", () => {
    const { root } = runComponent(Welcome, { name: "Zorg" });
    assert.equal(findByTestId(root, "welcome").children[0], "Hello, Zorg!", "EF_REACT_PROPS_DYNAMIC");
});
