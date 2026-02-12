import React, { createContext, useContext } from "react";

export const ThemeContext = createContext("light");

export function ThemeProvider({ theme, children }) {
    return React.createElement(
        ThemeContext.Provider,
        { value: theme },
        children
    );
}

export function ThemedButton() {
    const theme = useContext(ThemeContext);
    return React.createElement("button", { "data-testid": "btn" }, theme);
}
