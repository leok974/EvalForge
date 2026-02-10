# React Context: Theme

Edit `task.mjs`.

1. Create a Context (not exported).
2. Export `ThemeProvider` component:
   - Accept props `children` and `theme` (string).
   - Render the Context Provider with `value={theme}` surrounding the children.
3. Export `ThemedButton` component:
   - Consume the context `theme`.
   - Render a `button` with `data-testid="btn"`.
   - The button text should be the theme value.
