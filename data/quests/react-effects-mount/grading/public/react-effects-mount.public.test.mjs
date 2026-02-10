import test from "node:test";
import assert from "node:assert/strict";
import { runComponent } from "../../../_shared/react_test_helpers.mjs";
import { LifecycleLogger } from "../../workspace/task.mjs";

test("calls onMount but not onUnmount initially", () => {
    let mounted = 0;
    let unmounted = 0;

    runComponent(LifecycleLogger, {
        onMount: () => mounted++,
        onUnmount: () => unmounted++
    });

    assert.equal(mounted, 1, "EF_REACT_EFFECT_MOUNT");
    assert.equal(unmounted, 0, "EF_REACT_EFFECT_NO_UNMOUNT_YET");
});
