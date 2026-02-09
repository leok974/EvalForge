---
id: glossary/web/css/units
title: Units
world: web
level: beginner
tags: [css, measurement, layout]
related:
  - codex:glossary/web/css/typography
  - codex:glossary/web/css/box-model
---

# Units

## Definition
CSS units define sizes and spacing. Common units: `px`, `rem`, `em`, `%`, `vh`, `vw`. `rem` is typically best for scalable typography.

## Usage
- Use `rem` for font sizes and spacing scales.
- Use `%` for fluid layouts.
- Use `vh/vw` cautiously for mobile.

## Example
```css
.card { padding: 1rem; max-width: 60ch; }
```

## Pitfalls

* `vh` on mobile can behave unexpectedly due to browser UI bars.
* Mixing units without a system creates inconsistent spacing.

## Related

* Typography: rem units for text sizing.
* Box Model: units define padding/margin.