import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, act } from "../../../_shared/react_test_helpers.mjs";
import { ToggleButton } from "../../workspace/task.mjs";

test("toggles between ON and OFF", () => {
    const { root } = runComponent(ToggleButton);

    const btn = findByTestId(root, "toggle");
    assert.equal(btn.children[0], "OFF", "EF_REACT_TOGGLE_INIT");

    act(() => btn.props.onClick());
    assert.equal(btn.children[0], "ON", "EF_REACT_TOGGLE_ON");

    act(() => btn.props.onClick());
    assert.equal(btn.children[0], "OFF", "EF_REACT_TOGGLE_OFF");
});
