---
id: web/css/inheritance
title: CSS Inheritance
category: css
tags: [css, inheritance, basics]
---

# CSS Inheritance

Some CSS properties automatically pass from parent to child elements.

## Inherited Properties

These properties inherit by default:

- **Typography**: `color`, `font-family`, `font-size`, `font-weight`, `line-height`, `text-align`
- **List styles**: `list-style-type`
- **Cursor**: `cursor`
- **Visibility**: `visibility`

## Non-Inherited Properties

Most box model and layout properties don't inherit:

- `margin`, `padding`, `border`
- `width`, `height`
- `background`
- `position`, `display`
- `flex`, `grid` properties

## Controlling Inheritance

```css
/* Force inheritance */
.child {
  color: inherit;
}

/* Use initial browser default */
.element {
  color: initial;
}

/* Inherit from parent */
.element {
  all: inherit;
}

/* Reset to initial */
.element {
  all: initial;
}

/* Use natural value (inherit if inheritable, initial otherwise) */
.element {
  color: unset;
}
```

## Example

```css
body {
  font-family: Arial, sans-serif;
  color: #333;
}

/* All text inside body inherits font-family and color */
p { }  /* Gets Arial and #333 automatically */

/* Override inherited value */
.special {
  color: blue;
}
```

## Best Practices

- Set global typography on `body` or `html`
- Remember inheritance reduces repeated CSS
- Use `inherit` keyword when you need to force inheritance
- Don't rely on inheritance for layout properties
