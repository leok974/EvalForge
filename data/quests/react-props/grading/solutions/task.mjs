import React from "react";

export function Welcome({ name } = {}) {
    const safeName = name ?? "Stranger";
    return React.createElement("h1", { "data-testid": "welcome" }, `Hello, ${safeName}!`);
}
