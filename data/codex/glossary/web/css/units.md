---
id: web/css/units
title: CSS Units
category: css
tags: [css, units, measurements]
---

# CSS Units

CSS supports various units for sizing, spacing, and positioning.

## Absolute Units

Fixed size regardless of context:

- **`px`**: Pixels (most common)
- **`pt`**: Points (1pt = 1/72 inch)
- **`cm`**, **`mm`**, **`in`**: Physical units (rarely used)

## Relative Units

### Font-Relative

- **`em`**: Relative to parent font size
- **`rem`**: Relative to root (`<html>`) font size
- **`ex`**: x-height of font
- **`ch`**: Width of "0" character

### Viewport-Relative

- **`vw`**: 1% of viewport width
- **`vh`**: 1% of viewport height
- **`vmin`**: Smaller of vw or vh
- **`vmax`**: Larger of vw or vh

### Percentage

- **`%`**: Relative to parent element

## Usage Examples

```css
/* Pixels - precise control */
.box { width: 300px; }

/* REM - scalable typography */
html { font-size: 16px; }
h1 { font-size: 2rem; }     /* 32px */
p { font-size: 1rem; }      /* 16px */

/* EM - compound scaling */
.parent { font-size: 16px; }
.child { font-size: 1.5em; }  /* 24px (16 * 1.5) */

/* Viewport units - responsive */
.hero { height: 100vh; }      /* Full viewport height */
.sidebar { width: 20vw; }     /* 20% of viewport width */

/* Percentage - flexible */
.container { width: 80%; }    /* 80% of parent */
```

## Best Practices

- **Typography**: Use `rem` for consistency and accessibility
- **Spacing**: Use `rem` or `px`
- **Layout widths**: Use `%`, `vw`, or `fr` (grid)
- **Avoid `em` for spacing**: Can compound unexpectedly
- **Set base font size on `html`**: Makes `rem` predictable

## Common Patterns

```css
/* Responsive typography */
html { font-size: 16px; }
h1 { font-size: 2.5rem; }
p { font-size: 1rem; }
small { font-size: 0.875rem; }

/* Full-height sections */
section { min-height: 100vh; }

/* Flexible containers */
.container { width: 90%; max-width: 1200px; }
```
