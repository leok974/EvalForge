import React, { useState } from "react";

/**
 * TODO:
 * Export Counter().
 * - div data-testid="count" shows current count (starts at 0)
 * - button data-testid="inc" increments by 1
 * - button data-testid="reset" sets back to 0
 * No JSX.
 */
export function Counter() {
    const [count, _setCount] = useState(0);

    // TODO: implement
    const onInc = () => { };
    const onReset = () => { };

    return React.createElement(
        "div",
        { "data-testid": "counter" },
        React.createElement("div", { "data-testid": "count" }, String(count)),
        React.createElement("button", { "data-testid": "inc", onClick: onInc }, "Increment"),
        React.createElement("button", { "data-testid": "reset", onClick: onReset }, "Reset")
    );
}
