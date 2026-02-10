import React from 'react';

export function Welcome({ name }) {
    const target = name || "Stranger";
    return React.createElement('h1', { 'data-testid': 'welcome' }, `Hello, ${target}!`);
}
