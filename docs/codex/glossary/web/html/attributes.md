---
id: glossary/web/html/attributes
title: Attributes
world: web
level: beginner
tags: [html, attributes, syntax]
related:
  - codex:glossary/web/html/accessibility-basics
  - codex:glossary/web/html/images
  - codex:glossary/web/html/forms
---

# Attributes

## Definition
Attributes are key/value pairs on HTML elements that configure behavior and meaning (like `href`, `alt`, `type`, `name`). Some are global (`id`, `class`), others are element-specific.

## Usage
- `alt` for images, `name` for inputs, `href` for links.
- Data attributes (`data-*`) for hooks and metadata.
- ARIA attributes when needed for accessibility.

## Example
```html
<img src="/logo.png" alt="EvalForge logo" width="128" height="128" />
```

## Pitfalls

* Missing `alt` hurts accessibility and SEO.
* Duplicate `id` values break selectors and JS lookups.

## Related

* Accessibility Basics: attributes like alt improve accessibility.
* Images: images require alt attributes.
* Forms: form inputs use name attributes.