---
id: web/css/display
title: CSS Display Property
category: css
tags: [css, display, layout]
---

# CSS Display Property

The `display` property controls how elements are rendered in the layout.

## Common Values

### Block

```css
div { display: block; }
```

- Takes full width available
- Starts on new line
- Respects width/height
- Examples: `<div>`, `<p>`, `<h1>`-`<h6>`

### Inline

```css
span { display: inline; }
```

- Only takes needed width
- Stays on same line
- Ignores width/height
- Respects horizontal margin/padding only
- Examples: `<span>`, `<a>`, `<strong>`

### Inline-Block

```css
.button { display: inline-block; }
```

- Inline flow but respects width/height
- Best of both worlds
- Respects all margins and padding

### None

```css
.hidden { display: none; }
```

- Element removed from layout
- Not accessible to screen readers
- Use `visibility: hidden` to keep space

## Modern Layout Values

### Flex

```css
.container { display: flex; }
```

- One-dimensional layout (row or column)
- Powerful alignment controls

### Grid

```css
.container { display: grid; }
```

- Two-dimensional layout (rows and columns)
- Precise control over placement

## Visibility vs Display

```css
/* Hides but keeps space */
.invisible { visibility: hidden; }

/* Removes from layout */
.gone { display: none; }
```

## Best Practices

- Use semantic HTML first (it has default display values)
- Use `display: flex` or `grid` for layouts
- Use `display: none` carefully (affects accessibility)
- Understand block vs inline for flow control
