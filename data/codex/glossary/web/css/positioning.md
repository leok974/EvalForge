---
id: web/css/positioning
title: CSS Positioning
category: css
tags: [css, positioning, layout, z-index]
---

# CSS Positioning

Control element placement with the `position` property.

## Position Values

### Static (Default)

```css
.element {
  position: static;  /* Normal document flow */
}
```

### Relative

```css
.element {
  position: relative;
  top: 10px;     /* Offset from normal position */
  left: 20px;
}
```

- Stays in document flow
- Offsets are relative to original position
- Creates positioning context for absolute children

### Absolute

```css
.element {
  position: absolute;
  top: 0;
  right: 0;
}
```

- Removed from document flow
- Positioned relative to nearest positioned ancestor
- If no positioned ancestor, uses `<html>`

### Fixed

```css
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
}
```

- Removed from document flow
- Positioned relative to viewport
- Stays in place when scrolling

### Sticky

```css
.nav {
  position: sticky;
  top: 0;
}
```

- Hybrid: relative + fixed
- Acts relative until scroll threshold, then fixed
- Requires `top`, `bottom`, `left`, or `right`

## Offset Properties

```css
.positioned {
  top: 10px;
  right: 20px;
  bottom: 30px;
  left: 40px;
}
```

## Z-Index

Control stacking order of positioned elements:

```css
.element {
  position: relative;
  z-index: 10;  /* Higher = on top */
}
```

### Stacking Contexts

- Created by positioned elements with `z-index`
- Also created by `opacity < 1`, `transform`, `filter`, etc.
- Children stack within parent's context

```css
.parent {
  position: relative;
  z-index: 1;
}

.child {
  position: absolute;
  z-index: 999;  /* Only matters within parent context */
}
```

## Common Patterns

### Centering with Absolute

```css
.center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```

### Sticky Header

```css
.header {
  position: sticky;
  top: 0;
  background: white;
  z-index: 100;
}
```

### Modal Overlay

```css
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}
```

### Corner Badge

```css
.container {
  position: relative;
}

.badge {
  position: absolute;
  top: -10px;
  right: -10px;
}
```

### Full Coverage

```css
.overlay {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

/* Or shorthand */
.overlay {
  position: absolute;
  inset: 0;  /* Modern browsers */
}
```

## Best Practices

- Use `relative` to create positioning context
- Avoid `absolute` for layout (use Flexbox/Grid)
- Keep `z-index` values organized (increments of 10 or 100)
- Document stacking contexts in complex layouts
- Use `sticky` for scroll-aware elements
- Remember `position` affects document flow

## Z-Index Management

```css
:root {
  --z-dropdown: 100;
  --z-modal: 1000;
  --z-tooltip: 2000;
}

.dropdown { z-index: var(--z-dropdown); }
.modal { z-index: var(--z-modal); }
```
