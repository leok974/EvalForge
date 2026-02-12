import React from "react";

export function ToggleSection({ title, isVisible }) {
    const header = React.createElement("h2", null, title);

    const body = isVisible
        ? React.createElement("p", null, "Now you see me")
        : null;

    return React.createElement("div", { "data-testid": "toggle-section" }, header, body);
}
