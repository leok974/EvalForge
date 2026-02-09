---
id: glossary/web/css/backgrounds
title: Backgrounds
world: web
level: beginner
tags: [css, styling, design]
related:
  - codex:glossary/web/html/images
  - codex:glossary/web/css/colors
---

# Backgrounds

## Definition
Backgrounds control the visual fill behind an element (color, image, gradient). Backgrounds can be positioned, repeated, and sized.

## Usage
- Use gradients for subtle depth.
- Use `background-size: cover` for hero images.
- Control repeat/position intentionally.

## Example
```css
.hero {
  background: linear-gradient(180deg, rgba(0,0,0,.6), transparent);
}
```

## Pitfalls

* Background images don't support `alt` (use `<img>` when content matters).
* Heavy images hurt performance.

## Related

* Images: HTML images vs CSS backgrounds.
* Colors: backgrounds use colors.