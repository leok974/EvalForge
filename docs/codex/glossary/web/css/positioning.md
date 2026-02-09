---
id: glossary/web/css/positioning
title: Positioning
world: web
level: intermediate
tags: [css, layout, positioning]
related:
  - codex:glossary/web/css/box-model
  - codex:glossary/web/css/flexbox
---

# Positioning

## Definition
Positioning controls how an element is placed: `static`, `relative`, `absolute`, `fixed`, `sticky`. Absolute/fixed positioning removes elements from normal flow.

## Usage
- Tooltips/popovers (absolute).
- Sticky headers (sticky).
- Floating action buttons (fixed).

## Example
```css
.badge { position: absolute; top: 8px; right: 8px; }
.card { position: relative; }
```

## Pitfalls

* Absolute elements need a positioned parent (`position: relative`).
* Fixed elements can overlap content without padding.

## Related

* Box Model: positioning changes how box model works.
* Flexbox: flexbox is usually better than absolute positioning.