import React, { useState } from "react";

/**
 * TODO:
 * Export ToggleButton().
 * - button data-testid="toggle"
 * - Text is "OFF" initially, becomes "ON" on click, then "OFF" again, etc.
 * No JSX.
 */
export function ToggleButton() {
    const [_isOn, _setIsOn] = useState(false);

    // TODO: implement
    const onToggle = () => { };

    return React.createElement(
        "button",
        { "data-testid": "toggle", onClick: onToggle },
        "OFF"
    );
}
