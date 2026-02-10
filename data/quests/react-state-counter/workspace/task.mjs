import React, { useState } from 'react';

export function Counter() {
    const [count, setCount] = useState(0);

    return React.createElement('div', null,
        React.createElement('div', { 'data-testid': 'count' }, /* TODO */),
        React.createElement('button', { 'data-testid': 'increment' }, '+1'),
        React.createElement('button', { 'data-testid': 'reset' }, 'Reset')
    );
}
