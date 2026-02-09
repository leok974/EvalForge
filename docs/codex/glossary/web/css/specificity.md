---
id: glossary/web/css/specificity
title: Specificity
world: web
level: intermediate
tags: [css, specificity, debugging]
related:
  - codex:glossary/web/css/cascade
  - codex:glossary/web/css/selectors
---

# Specificity

## Definition
Specificity determines which CSS rule wins when multiple match. IDs > classes/attributes > elements. Later rules also matter when specificity ties.

## Usage
- Keep specificity low and consistent.
- Use classes instead of IDs for styling.
- Use `!important` only as a last resort.

## Example
```css
/* .card wins over div */
div { padding: 8px; }
.card { padding: 16px; }
```

## Pitfalls

* IDs in CSS create "specificity wars".
* `!important` can become contagious and unmaintainable.

## Related

* Cascade: specificity is part of the cascade.
* Selectors: selectors have different specificity.