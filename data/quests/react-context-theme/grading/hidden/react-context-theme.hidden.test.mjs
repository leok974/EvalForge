import test from "node:test";
import assert from "node:assert/strict";
import React from "react";
import { runComponent, findByTestId } from "../../../_shared/react_test_helpers.mjs";
import { ThemeProvider, ThemedButton } from "../../workspace/task.mjs";

test("dynamic theme updates", () => {
    const Wrapper = () => React.createElement(
        ThemeProvider,
        { theme: "blue" },
        React.createElement(ThemedButton)
    );
    const { root } = runComponent(Wrapper);
    assert.equal(findByTestId(root, "btn").children[0], "blue", "EF_REACT_CONTEXT_DYNAMIC");
});
