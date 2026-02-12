import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, act } from "../../../_shared/react_test_helpers.mjs";
import { LifecycleLogger } from "../../workspace/task.mjs";

test("onMount called once after mount; onUnmount only on unmount", () => {
    let mountCalls = 0;
    let unmountCalls = 0;

    const onMount = () => { mountCalls += 1; };
    const onUnmount = () => { unmountCalls += 1; };

    const { renderer } = runComponent(LifecycleLogger, { onMount, onUnmount });

    assert.equal(mountCalls, 1);
    assert.equal(unmountCalls, 0);

    act(() => renderer.unmount());
    assert.equal(unmountCalls, 1);
});
