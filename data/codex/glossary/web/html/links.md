---
id: web/html/links
title: HTML Links
category: html
tags: [html, links, navigation]
---

# HTML Links

The `<a>` (anchor) element creates hyperlinks to other pages, files, or locations.

## Basic Syntax

```html
<a href="https://example.com">Link Text</a>
```

## Key Attributes

- **`href`**: Destination URL (required)
- **`target`**: Where to open link
  - `_self`: Same window (default)
  - `_blank`: New tab/window
- **`rel`**: Relationship/security
  - `noopener`: Prevent window.opener access
  - `noreferrer`: Hide referrer information

## Link Types

**External links:**
```html
<a href="https://example.com" target="_blank" rel="noopener">External</a>
```

**Internal links:**
```html
<a href="/about">About Page</a>
```

**Anchor links:**
```html
<a href="#section-id">Jump to Section</a>
```

**Email links:**
```html
<a href="mailto:email@example.com">Email Us</a>
```

## Best Practices

- Always provide descriptive link text
- Use `rel="noopener"` with `target="_blank"`
- Avoid "click here" - describe the destination
