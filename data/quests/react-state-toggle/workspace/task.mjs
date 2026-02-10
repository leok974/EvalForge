import React, { useState } from 'react';

export function ToggleButton() {
    return React.createElement('button', { 'data-testid': 'toggle' }, 'OFF');
}
