---
id: glossary/web/css/media-queries
title: Media Queries
world: web
level: intermediate
tags: [css, responsive, media-queries]
related:
  - codex:glossary/web/css/grid
  - codex:glossary/web/css/units
---

# Media Queries

## Definition
Media queries apply CSS based on device conditions (width, prefers-color-scheme, reduced motion). They drive responsive design.

## Usage
- Adjust layout at breakpoints.
- Respect reduced-motion preferences.
- Adapt typography for small screens.

## Example
```css
@media (max-width: 720px) {
  .sidebar { display: none; }
}
```

## Pitfalls

* Too many breakpoints makes maintenance hard.
* Mobile-first styles usually scale better than desktop-first.

## Related

* Grid: grid works with media queries for responsive layouts.
* Units: viewport units interact with media queries.