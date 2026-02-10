# Hints — React Context: Theme

## Hint 1 (nudge)
Wrap children with the Provider and set `value` to the `theme` prop.

## Hint 2 (more specific)
`ThemeContext.Provider` is just a React component:
- type: `ThemeContext.Provider`
- props: `{ value: theme }`
- child: `children`

## Hint 3 (close)
Provider:
- `React.createElement(ThemeContext.Provider, { value: theme }, children)`

Consumer:
- `const theme = useContext(ThemeContext);`
- `React.createElement("button", { "data-testid": "btn" }, theme)`
