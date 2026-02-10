import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, act } from "../../../_shared/react_test_helpers.mjs";
import { ShoppingCart } from "../../workspace/task.mjs";

test("resets total", () => {
    const { root } = runComponent(ShoppingCart);
    const total = findByTestId(root, "total");
    const add10 = findByTestId(root, "add-10");
    const reset = findByTestId(root, "reset");

    act(() => add10.props.onClick());
    assert.equal(total.children[0], "10");

    act(() => reset.props.onClick());
    assert.equal(total.children[0], "0", "EF_REACT_REDUCER_RESET");
});
