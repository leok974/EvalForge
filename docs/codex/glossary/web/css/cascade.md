---
id: glossary/web/css/cascade
title: Cascade
world: web
level: intermediate
tags: [css, cascade, fundamentals]
related:
  - codex:glossary/web/css/specificity
  - codex:glossary/web/css/inheritance
---

# Cascade

## Definition
The cascade is how CSS decides final styles: origin (browser/user/author), importance, specificity, and source order.

## Usage
- Structure styles to reduce conflicts.
- Place overrides later intentionally.
- Use component-level styling patterns.

## Example
```css
.card { color: white; }
.theme-light .card { color: black; } /* later override */
```

## Pitfalls

* Random import order causes unpredictable styling.
* Overriding without understanding specificity leads to hacks.

## Related

* Specificity: specificity is part of the cascade.
* Inheritance: inheritance interacts with the cascade.