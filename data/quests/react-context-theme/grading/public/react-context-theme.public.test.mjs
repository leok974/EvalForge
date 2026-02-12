import test from "node:test";
import assert from "node:assert/strict";
import React from "react";
import { runComponent, findByTestId, textContent } from "../../../_shared/react_test_helpers.mjs";
import { ThemeProvider, ThemedButton } from "../../workspace/task.mjs";

test("ThemeProvider provides theme value to ThemedButton", () => {
    function App() {
        return React.createElement(
            ThemeProvider,
            { theme: "dark" },
            React.createElement(ThemedButton)
        );
    }

    const { root } = runComponent(App);
    const btn = findByTestId(root, "btn");
    assert.equal(textContent(btn), "dark");
});

test("ThemedButton uses default theme when no provider present", () => {
    const { root } = runComponent(ThemedButton);
    const btn = findByTestId(root, "btn");
    assert.equal(textContent(btn), "light");
});
