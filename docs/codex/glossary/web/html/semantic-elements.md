---
id: glossary/web/html/semantic-elements
title: Semantic Elements
world: web
level: beginner
tags: [html, semantics, structure]
related:
  - codex:glossary/web/html/document-skeleton
  - codex:glossary/web/html/accessibility-basics
---

# Semantic Elements

## Definition
Semantic elements describe meaning/role: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`. They improve accessibility, SEO, and maintainability.

## Usage
- Use `<main>` for primary content (once per page).
- Wrap site navigation in `<nav>`.
- Use headings (`h1..h6`) in order.

## Example
```html
<header><nav>...</nav></header>
<main>
  <h1>Workshop</h1>
</main>
<footer>©</footer>
```

## Pitfalls

* Multiple `<main>` elements is invalid.
* Skipping heading levels can confuse readers.

## Related

* Document Skeleton: semantic elements structure the body.
* Accessibility Basics: semantic HTML improves accessibility.