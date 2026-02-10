import test from "node:test";
import assert from "node:assert/strict";
import React from "react";
import { runComponent, findByTestId } from "../../../_shared/react_test_helpers.mjs";
import { ThemeProvider, ThemedButton } from "../../workspace/task.mjs";

test("button consumes theme from provider", () => {
    // We render Provider -> Button
    // We can't use runComponent directly on just Button if we need wrapper
    // But runComponent takes Component, so we can pass a wrapper component

    const Wrapper = () => React.createElement(
        ThemeProvider,
        { theme: "dark" },
        React.createElement(ThemedButton)
    );

    const { root } = runComponent(Wrapper);
    const btn = findByTestId(root, "btn");

    assert.equal(btn.children[0], "dark", "EF_REACT_CONTEXT_CONSUME");
});
