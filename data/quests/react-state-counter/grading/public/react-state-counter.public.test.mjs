import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, act } from "../../../_shared/react_test_helpers.mjs";
import { Counter } from "../../workspace/task.mjs";

test("increments counter", () => {
    const { root } = runComponent(Counter);

    const countDiv = findByTestId(root, "count");
    const btn = findByTestId(root, "increment");

    assert.equal(countDiv.children[0], "0", "EF_REACT_STATE_INIT");

    act(() => {
        btn.props.onClick();
    });

    assert.equal(countDiv.children[0], "1", "EF_REACT_STATE_INC");

    act(() => {
        btn.props.onClick();
    });

    assert.equal(countDiv.children[0], "2", "EF_REACT_STATE_INC_2");
});
