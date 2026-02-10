import React, { useState } from 'react';

export function Counter() {
    const [count, setCount] = useState(0);

    return React.createElement('div', null,
        React.createElement('div', { 'data-testid': 'count' }, String(count)),
        React.createElement('button', {
            'data-testid': 'increment',
            onClick: () => setCount(c => c + 1)
        }, '+1'),
        React.createElement('button', {
            'data-testid': 'reset',
            onClick: () => setCount(0)
        }, 'Reset')
    );
}
