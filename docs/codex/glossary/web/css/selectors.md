---
id: glossary/web/css/selectors
title: Selectors
world: web
level: beginner
tags: [css, selectors, syntax]
related:
  - codex:glossary/web/css/specificity
  - codex:glossary/web/css/cascade
---

# Selectors

## Definition
Selectors choose which elements a CSS rule applies to (class, id, element, attribute, pseudo-class). Good selector strategy keeps styles maintainable.

## Usage
- Prefer class selectors for reusable styling.
- Use `:hover`, `:focus-visible` for states.
- Avoid deep nesting unless necessary.

## Example
```css
.button { padding: .5rem 1rem; }
.button:hover { transform: translateY(-1px); }
```

## Pitfalls

* Over-specific selectors make overrides hard.
* Styling by tag alone can cause unintended global changes.

## Related

* Specificity: selectors combine with specificity.
* Cascade: selectors interact with the cascade.