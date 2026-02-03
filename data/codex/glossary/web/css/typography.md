---
id: web/css/typography
title: CSS Typography
category: css
tags: [css, typography, fonts, text]
---

# CSS Typography

Control text appearance and readability with CSS typography properties.

## Font Properties

```css
.text {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 16px;
  font-weight: 400;      /* 100-900, or normal/bold */
  font-style: normal;    /* normal, italic, oblique */
  line-height: 1.5;      /* Unitless multiplier preferred */
  letter-spacing: 0.5px;
  word-spacing: 2px;
}
```

## Font Families

```css
/* System fonts (fast, reliable) */
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

/* Web fonts */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700');
font-family: 'Roboto', sans-serif;

/* Generic families (fallback) */
font-family: serif;      /* Times New Roman */
font-family: sans-serif; /* Arial, Helvetica */
font-family: monospace;  /* Courier */
```

## Text Styling

```css
.text {
  color: #333;
  text-align: left;        /* left, center, right, justify */
  text-decoration: none;   /* none, underline, line-through */
  text-transform: uppercase; /* uppercase, lowercase, capitalize */
  text-indent: 2em;
}
```

## Line Height

```css
/* Bad: fixed units */
p { line-height: 24px; }

/* Good: unitless multiplier */
p { line-height: 1.5; }  /* 1.5 × font-size */
```

## Font Weight Scale

- `100`: Thin
- `300`: Light
- `400`: Normal (default)
- `500`: Medium
- `700`: Bold
- `900`: Black

## Web Font Loading

```css
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2') format('woff2'),
       url('font.woff') format('woff');
  font-weight: 400;
  font-style: normal;
  font-display: swap;  /* Show fallback until font loads */
}
```

## Responsive Typography

```css
/* Fluid typography */
html {
  font-size: 16px;
}

@media (min-width: 768px) {
  html { font-size: 18px; }
}

/* Or use clamp() */
h1 {
  font-size: clamp(1.5rem, 5vw, 3rem);
}
```

## Best Practices

- Use unitless `line-height` (typically 1.4-1.6)
- Limit font families to 2-3 per site
- Use system fonts for performance
- Set base size on `html`, use `rem` for scaling
- Ensure sufficient contrast (4.5:1 minimum)
- Optimize web font loading with `font-display: swap`
