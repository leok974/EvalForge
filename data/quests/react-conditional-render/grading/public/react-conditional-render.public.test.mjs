import test from "node:test";
import assert from "node:assert/strict";
import { runComponent } from "../../../_shared/react_test_helpers.mjs";
import { ToggleSection } from "../../workspace/task.mjs";

test("renders title and content when visible", () => {
    const { root } = runComponent(ToggleSection, { title: "Secret", isVisible: true });

    const h2 = root.findByType("h2");
    assert.equal(h2.children[0], "Secret", "EF_REACT_COND_TITLE");

    const p = root.findByType("p");
    assert.equal(p.children[0], "Now you see me", "EF_REACT_COND_VISIBLE");
});
