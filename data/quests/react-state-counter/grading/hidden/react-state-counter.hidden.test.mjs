import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, act } from "../../../_shared/react_test_helpers.mjs";
import { Counter } from "../../workspace/task.mjs";

test("resets counter", () => {
    const { root } = runComponent(Counter);
    const countDiv = findByTestId(root, "count");
    const inc = findByTestId(root, "increment");
    const reset = findByTestId(root, "reset");

    act(() => {
        inc.props.onClick();
        inc.props.onClick();
    });
    assert.equal(countDiv.children[0], "2");

    act(() => {
        reset.props.onClick();
    });
    assert.equal(countDiv.children[0], "0", "EF_REACT_STATE_RESET");
});
