import test from "node:test";
import assert from "node:assert/strict";
import { runComponent } from "../../../_shared/react_test_helpers.mjs";
import { ToggleSection } from "../../workspace/task.mjs";

test("hides content when not visible", () => {
    const { root } = runComponent(ToggleSection, { title: "Hidden", isVisible: false });

    const h2 = root.findByType("h2");
    assert.equal(h2.children[0], "Hidden");

    try {
        root.findByType("p");
        assert.fail("EF_REACT_COND_HIDDEN: p tag should not exist");
    } catch (e) {
        // Expected error from findByType logic if missing
        assert.match(e.message, /No instances found/, "EF_REACT_COND_HIDDEN");
    }
});
