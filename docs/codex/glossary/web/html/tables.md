---
id: glossary/web/html/tables
title: Tables
world: web
level: beginner
tags: [html, data-display, semantics]
related:
  - codex:glossary/web/html/accessibility-basics
  - codex:glossary/web/css/typography
---

# Tables

## Definition
Tables display tabular data with rows and columns. Use `<thead>` for headers and `<tbody>` for body rows.

## Usage
- Data grids, comparisons, reports.
- Use header cells `<th>` for column/row headings.
- Add captions for accessibility when needed.

## Example
```html
<table>
  <thead><tr><th>Quest</th><th>Status</th></tr></thead>
  <tbody>
    <tr><td>Ignition</td><td>Unlocked</td></tr>
  </tbody>
</table>
```

## Pitfalls

* Don't use tables for page layout (use flex/grid instead).
* Missing `<th>` hurts accessibility.

## Related

* Accessibility Basics: accessible tables use proper markup.
* Typography: table text uses typography styling.