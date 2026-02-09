---
id: glossary/web/html/tags-and-elements
title: Tags And Elements
world: web
level: beginner
tags: [html, fundamentals, syntax]
related:
  - codex:glossary/web/html/attributes
  - codex:glossary/web/html/semantic-elements
  - codex:glossary/web/html/links
---

# Tags And Elements

## Definition
A tag is the syntax (`<p>`), an element is the actual node in the DOM (opening tag + content + closing tag). Elements can have attributes and nested children.

## Usage
- Use elements to structure content and provide meaning.
- Combine semantic elements with appropriate attributes.
- Inspect elements in DevTools to debug layout.

## Example
```html
<a href="/docs" rel="noopener">Docs</a>
```

## Pitfalls

* Overusing `<div>` makes pages less accessible and harder to style.
* Invalid nesting can cause unexpected rendering.

## Related

* Attributes: elements have attributes.
* Semantic Elements: semantic tags provide meaning.
* Links: links are anchor elements.