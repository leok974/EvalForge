---
id: glossary/web/css/grid
title: Grid
world: web
level: intermediate
tags: [css, layout, grid]
related:
  - codex:glossary/web/css/flexbox
  - codex:glossary/web/css/box-model
---

# Grid

## Definition
CSS Grid is a 2D layout system for rows and columns. It's ideal for dashboards, cards, and page shells.

## Usage
- Define column tracks with `grid-template-columns`.
- Control gaps consistently.
- Create responsive layouts with `minmax` and `auto-fit`.

## Example
```css
.grid { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }
```

## Pitfalls

* Overusing fixed widths harms responsiveness.
* Too many nested grids can become hard to reason about.

## Related

* Flexbox: flexbox is 1D; grid is 2D.
* Box Model: grid builds on box model.