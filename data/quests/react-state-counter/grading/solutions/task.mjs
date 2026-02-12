import React, { useState } from "react";

export function Counter() {
    const [count, setCount] = useState(0);

    const onInc = () => setCount((c) => c + 1);
    const onReset = () => setCount(0);

    return React.createElement(
        "div",
        { "data-testid": "counter" },
        React.createElement("div", { "data-testid": "count" }, String(count)),
        React.createElement("button", { "data-testid": "inc", onClick: onInc }, "Increment"),
        React.createElement("button", { "data-testid": "reset", onClick: onReset }, "Reset")
    );
}
