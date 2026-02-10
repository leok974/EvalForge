import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, act } from "../../../_shared/react_test_helpers.mjs";
import { ShoppingCart } from "../../workspace/task.mjs";

test("adds values to total", () => {
    const { root } = runComponent(ShoppingCart);
    const total = findByTestId(root, "total");
    const add10 = findByTestId(root, "add-10");

    assert.equal(total.children[0], "0", "EF_REACT_REDUCER_INIT");

    act(() => add10.props.onClick());
    assert.equal(total.children[0], "10", "EF_REACT_REDUCER_ADD");

    act(() => add10.props.onClick());
    assert.equal(total.children[0], "20", "EF_REACT_REDUCER_ADD_2");
});
