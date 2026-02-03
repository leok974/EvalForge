---
id: web/css/backgrounds
title: CSS Backgrounds
category: css
tags: [css, backgrounds, design]
---

# CSS Backgrounds

Control element backgrounds with colors, images, gradients, and more.

## Background Color

```css
.box {
  background-color: #f0f0f0;
  background-color: rgba(0, 0, 0, 0.5);
}
```

## Background Images

```css
.hero {
  background-image: url('image.jpg');
  background-size: cover;           /* cover, contain, or dimensions */
  background-position: center;      /* x y, or keywords */
  background-repeat: no-repeat;     /* repeat, repeat-x, repeat-y, no-repeat */
  background-attachment: fixed;     /* scroll, fixed, local */
}
```

## Background Shorthand

```css
.element {
  background: #333 url('bg.jpg') no-repeat center/cover;
  /*          color image         repeat    position/size */
}
```

## Multiple Backgrounds

```css
.layered {
  background:
    url('overlay.png') no-repeat top right,
    url('background.jpg') no-repeat center/cover;
}
```

## Gradients

### Linear Gradients

```css
.gradient {
  background: linear-gradient(to right, #ff0000, #00ff00);
  background: linear-gradient(45deg, red, blue);
  background: linear-gradient(to bottom, red 0%, blue 100%);
}
```

### Radial Gradients

```css
.radial {
  background: radial-gradient(circle, red, blue);
  background: radial-gradient(ellipse at top, red, blue);
}
```

### Conic Gradients

```css
.conic {
  background: conic-gradient(red, yellow, green, blue, red);
}
```

## Background Size

```css
.cover { background-size: cover; }      /* Fill container, may crop */
.contain { background-size: contain; }  /* Fit container, may have gaps */
.custom { background-size: 50% auto; }  /* Custom dimensions */
```

## Background Position

```css
.positioned {
  background-position: top right;
  background-position: center center;
  background-position: 10px 20px;
  background-position: 50% 50%;
}
```

## Background Clip & Origin

```css
.clipped {
  background-clip: border-box;    /* default */
  background-clip: padding-box;
  background-clip: content-box;
  background-clip: text;          /* Clip to text shape */
}

.origin {
  background-origin: border-box;
  background-origin: padding-box;
  background-origin: content-box;
}
```

## Best Practices

- Optimize image file sizes
- Provide fallback colors
- Use `background-size: cover` for full backgrounds
- Consider mobile performance (large images)
- Use gradients for modern effects
- Ensure text remains readable over backgrounds

## Common Patterns

```css
/* Hero section */
.hero {
  background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
              url('hero.jpg') no-repeat center/cover;
  color: white;
}

/* Subtle pattern */
.pattern {
  background: #f0f0f0 url('pattern.png') repeat;
}
```
