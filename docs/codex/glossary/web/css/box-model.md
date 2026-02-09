---
id: glossary/web/css/box-model
title: Box Model
world: web
level: beginner
tags: [css, layout, fundamentals]
related:
  - codex:glossary/web/css/positioning
  - codex:glossary/web/css/flexbox
---

# Box Model

## Definition
The box model describes how elements take space: content + padding + border + margin. It determines layout sizing and spacing.

## Usage
- Use padding for internal spacing.
- Use margin for external spacing.
- Prefer `box-sizing: border-box` for predictable sizing.

## Example
```css
* { box-sizing: border-box; }
.box { width: 200px; padding: 16px; border: 1px solid; margin: 12px; }
```

## Pitfalls

* Without border-box, padding/border increase total width unexpectedly.
* Collapsing margins can surprise you in vertical layouts.

## Related

* Positioning: positioning changes how box model interacts with layout.
* Flexbox: flexbox builds on the box model.