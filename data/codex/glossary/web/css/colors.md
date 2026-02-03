---
id: web/css/colors
title: CSS Colors
category: css
tags: [css, colors, design]
---

# CSS Colors

CSS provides multiple ways to specify colors.

## Color Formats

### Named Colors

```css
color: red;
color: steelblue;
color: transparent;
```

140+ named colors available.

### Hexadecimal

```css
color: #ff0000;      /* Red */
color: #f00;         /* Shorthand */
color: #ff0000ff;    /* With alpha */
```

### RGB / RGBA

```css
color: rgb(255, 0, 0);           /* Red */
color: rgba(255, 0, 0, 0.5);     /* 50% transparent red */
```

### HSL / HSLA

```css
color: hsl(0, 100%, 50%);        /* Red */
color: hsla(0, 100%, 50%, 0.5);  /* 50% transparent red */
```

- **H**: Hue (0-360 degrees)
- **S**: Saturation (0-100%)
- **L**: Lightness (0-100%)

## Modern Color Spaces

```css
/* LCH - perceptually uniform */
color: lch(50% 100 0);

/* LAB */
color: lab(50% 125 -125);
```

## CSS Variables for Colors

```css
:root {
  --primary-color: #007bff;
  --text-color: #333;
  --bg-color: #fff;
}

.element {
  color: var(--primary-color);
  background: var(--bg-color);
}
```

## Opacity

```css
/* Entire element */
.box { opacity: 0.5; }

/* Just background */
.box { background: rgba(0, 0, 0, 0.5); }
```

## Color Keywords

```css
color: currentColor;  /* Inherits color value */
background: transparent;
```

## Accessibility

```css
/* Ensure sufficient contrast */
.text {
  color: #333;           /* Dark text */
  background: #fff;      /* Light background */
  /* Contrast ratio: 12.6:1 ✅ */
}
```

**WCAG Requirements:**
- Normal text: 4.5:1 minimum
- Large text (18pt+ or 14pt+ bold): 3:1 minimum

## Best Practices

- Define color palette with CSS variables
- Use HSL for easier color manipulation
- Ensure accessibility with contrast checkers
- Limit palette to maintain consistency
- Use semantic color names (`--primary`, `--danger`)

## Common Patterns

```css
:root {
  /* Brand colors */
  --primary: #007bff;
  --secondary: #6c757d;
  --success: #28a745;
  --danger: #dc3545;
  --warning: #ffc107;
  
  /* Neutral colors */
  --gray-100: #f8f9fa;
  --gray-900: #212529;
}
```
