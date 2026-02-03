---
id: web/html/attributes
title: HTML Attributes
category: html
tags: [html, attributes, syntax]
---

# HTML Attributes

Attributes provide additional information about HTML elements.

## Syntax

```html
<element attribute="value">
```

## Common Attributes

**Global** (work on any element):
- `id`: Unique identifier
- `class`: CSS class names (space-separated)
- `style`: Inline CSS
- `title`: Tooltip text
- `lang`: Language code

**Element-specific**:
- `href` (links): URL destination
- `src` (images): Image source
- `alt` (images): Alternative text
- `type` (inputs): Input type
- `name` (forms): Form field name

## Boolean Attributes

Some attributes don't need values:

```html
<input disabled>
<input required checked>
```

## Best Practices

- Use double quotes for values
- Prefer semantic HTML over excessive styling
- Always include `alt` on images
