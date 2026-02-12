import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, act, textContent } from "../../../_shared/react_test_helpers.mjs";
import { ToggleButton } from "../../workspace/task.mjs";

test("ToggleButton swaps OFF <-> ON on click", () => {
    const { root } = runComponent(ToggleButton);

    const btn = findByTestId(root, "toggle");
    assert.equal(textContent(btn), "OFF");

    act(() => btn.props.onClick());
    assert.equal(textContent(findByTestId(root, "toggle")), "ON");

    act(() => btn.props.onClick());
    assert.equal(textContent(findByTestId(root, "toggle")), "OFF");
});
