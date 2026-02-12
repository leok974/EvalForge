import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, act, textContent } from "../../../_shared/react_test_helpers.mjs";
import { Counter } from "../../workspace/task.mjs";

test("Counter increments and resets deterministically", () => {
    const { root } = runComponent(Counter);

    const countNode = findByTestId(root, "count");
    assert.equal(textContent(countNode), "0");

    const inc = findByTestId(root, "inc");
    act(() => inc.props.onClick());
    assert.equal(textContent(findByTestId(root, "count")), "1");

    act(() => inc.props.onClick());
    assert.equal(textContent(findByTestId(root, "count")), "2");

    const reset = findByTestId(root, "reset");
    act(() => reset.props.onClick());
    assert.equal(textContent(findByTestId(root, "count")), "0");
});
