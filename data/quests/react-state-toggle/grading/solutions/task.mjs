import React, { useState } from "react";

export function ToggleButton() {
    const [isOn, setIsOn] = useState(false);

    const onToggle = () => setIsOn((v) => !v);

    return React.createElement(
        "button",
        { "data-testid": "toggle", onClick: onToggle },
        isOn ? "ON" : "OFF"
    );
}
