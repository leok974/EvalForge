import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, textContent } from "../../../_shared/react_test_helpers.mjs";
import { ToggleSection } from "../../workspace/task.mjs";

test("h2 always renders with title text", () => {
    const { root } = runComponent(ToggleSection, { title: "Controls", isVisible: false });
    const h2 = root.findByType("h2");
    assert.equal(textContent(h2), "Controls");
});

test("p renders when isVisible=true", () => {
    const { root } = runComponent(ToggleSection, { title: "Controls", isVisible: true });
    const p = root.findByType("p");
    assert.equal(textContent(p), "Now you see me");
});

test("p does NOT render when isVisible=false", () => {
    const { root } = runComponent(ToggleSection, { title: "Controls", isVisible: false });
    const ps = root.findAllByType("p");
    assert.equal(ps.length, 0);
});
