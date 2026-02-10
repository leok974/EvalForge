import React, { useState } from 'react';

export function ToggleButton() {
    const [on, setOn] = useState(false);
    return React.createElement('button', {
        'data-testid': 'toggle',
        onClick: () => setOn(v => !v)
    }, on ? 'ON' : 'OFF');
}
