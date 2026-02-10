import React, { createContext, useContext } from 'react';

const ThemeContext = createContext('light');

export function ThemeProvider({ children, theme }) {
    // TODO: Provider
    return React.createElement(React.Fragment, null, children);
}

export function ThemedButton() {
    // TODO: useContext
    return React.createElement('button', { 'data-testid': 'btn' }, 'default');
}
