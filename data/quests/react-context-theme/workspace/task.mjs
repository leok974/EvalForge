import React, { createContext, useContext } from "react";

/**
 * TODO:
 * Create ThemeContext with default "light"
 * Export:
 * - ThemeProvider({ theme, children }) -> provides theme via context
 * - ThemedButton() -> reads theme from context, renders:
 *   <button data-testid="btn">{theme}</button>
 * No JSX.
 */
export const ThemeContext = createContext("light");

export function ThemeProvider(_props) {
    return null;
}

export function ThemedButton() {
    const theme = useContext(ThemeContext);
    return React.createElement("button", { "data-testid": "btn" }, theme);
}
