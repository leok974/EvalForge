import test from "node:test";
import assert from "node:assert/strict";
import { runComponent } from "../../../_shared/react_test_helpers.mjs";
import { LifecycleLogger } from "../../workspace/task.mjs";

test("calls onUnmount when unmounted", () => {
    let unmounted = 0;
    // react-test-renderer's unmount() triggers cleanup
    const { root } = runComponent(LifecycleLogger, {
        onMount: () => { },
        onUnmount: () => unmounted++
    });

    // We can't easily unmount via helper unless we return the renderer instance from runComponent.
    // runComponent returns { root, toJSON, instance } but not the 'renderer' itself which has unmount().
    // Actually TestRenderer.create() returns the renderer.
    // We need to update runComponent or use raw TestRenderer here. 
    // Wait, I updated runComponent to return root, but I capture `root` variable inside act.
    // Let's assume for this specific test we might need `renderer.unmount()`.
    // I will check if I can just use raw create here since `runComponent` hides the renderer instance.

    // Actually, let's update runComponent in _shared later to return 'renderer', or assume it's exposed.
    // No, `root` is `TestRenderer.root`.
    // I'll reimplement this test using raw TestRenderer imports + act, since it's a specific lifecycle test.
    // Or I can update runComponent now.
});

// Re-writing content to include raw implementation for unmount testing
import React from 'react';
import TestRenderer from 'react-test-renderer';
const { act } = TestRenderer;

test("calls onUnmount when unmounted", () => {
    let unmounted = 0;
    let renderer;

    act(() => {
        renderer = TestRenderer.create(React.createElement(LifecycleLogger, {
            onMount: () => { },
            onUnmount: () => unmounted++
        }));
    });

    act(() => {
        renderer.unmount();
    });

    assert.equal(unmounted, 1, "EF_REACT_EFFECT_UNMOUNT");
});
