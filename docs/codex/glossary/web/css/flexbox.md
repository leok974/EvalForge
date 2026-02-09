---
id: glossary/web/css/flexbox
title: Flexbox
world: web
level: beginner
tags: [css, layout, flexbox]
related:
  - codex:glossary/web/css/grid
  - codex:glossary/web/css/box-model
---

# Flexbox

## Definition
Flexbox is a 1D layout system for arranging items in a row or column. It excels at alignment, spacing, and responsive distribution.

## Usage
- Horizontal nav bars and toolbars.
- Centering content.
- Responsive wrapping rows.

## Example
```css
.row { display: flex; gap: 12px; align-items: center; }
.row > .spacer { flex: 1; }
```

## Pitfalls

* Flex is 1D; use Grid for 2D layouts.
* Forgetting `min-width: 0` can cause overflow in flex children.

## Related

* Grid: grid is 2D layout; flexbox is 1D.
* Box Model: flexbox builds on box model.