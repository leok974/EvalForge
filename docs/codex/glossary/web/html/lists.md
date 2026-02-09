---
id: glossary/web/html/lists
title: Lists
world: web
level: beginner
tags: [html, structure, semantics]
related:
  - codex:glossary/web/html/semantic-elements
  - codex:glossary/web/css/typography
---

# Lists

## Definition
Lists group related items. Use `<ul>` for unordered lists and `<ol>` for ordered steps. `<li>` must be inside a list container.

## Usage
- Navigation menus, bullet points, step-by-step instructions.
- Use `<ol>` for sequences that matter.
- Nest lists for hierarchy.

## Example
```html
<ol>
  <li>Install deps</li>
  <li>Run dev server</li>
  <li>Open Workshop</li>
</ol>
```

## Pitfalls

* Replacing lists with `<div>` loses semantics and accessibility.
* Incorrect nesting breaks layout and screen readers.

## Related

* Semantic Elements: lists are semantic HTML.
* Typography: list styling uses typography principles.