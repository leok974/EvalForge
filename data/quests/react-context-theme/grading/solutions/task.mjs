import React, { createContext, useContext } from 'react';

const ThemeContext = createContext('light');

export function ThemeProvider({ children, theme }) {
    return React.createElement(ThemeContext.Provider, { value: theme }, children);
}

export function ThemedButton() {
    const theme = useContext(ThemeContext);
    return React.createElement('button', { 'data-testid': 'btn' }, theme);
}
