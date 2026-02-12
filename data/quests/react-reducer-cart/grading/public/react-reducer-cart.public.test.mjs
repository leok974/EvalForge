import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, act, textContent } from "../../../_shared/react_test_helpers.mjs";
import { ShoppingCart } from "../../workspace/task.mjs";

test("ShoppingCart increments by 10 and resets via reducer actions", () => {
    const { root } = runComponent(ShoppingCart);

    assert.equal(textContent(findByTestId(root, "total")), "0");

    const add10 = findByTestId(root, "add-10");
    act(() => add10.props.onClick());
    assert.equal(textContent(findByTestId(root, "total")), "10");

    act(() => add10.props.onClick());
    assert.equal(textContent(findByTestId(root, "total")), "20");

    const reset = findByTestId(root, "reset");
    act(() => reset.props.onClick());
    assert.equal(textContent(findByTestId(root, "total")), "0");
});
