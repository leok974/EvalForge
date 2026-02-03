---
id: web/html/tags-and-elements
title: HTML Tags and Elements
category: html
tags: [html, basics, syntax]
---

# HTML Tags and Elements

HTML uses **tags** to create **elements** that structure content.

## Syntax

```html
<tagname attribute="value">Content</tagname>
```

## Components

- **Opening tag**: `<tagname>`
- **Content**: Text or nested elements
- **Closing tag**: `</tagname>`
- **Self-closing**: `<img />`, `<br />`, `<input />`

## Nesting Rules

Elements must be properly nested:

```html
<!-- Correct -->
<div><p>Text</p></div>

<!-- Incorrect -->
<div><p>Text</div></p>
```

## Common Tags

- `<div>`, `<span>`: Generic containers
- `<p>`: Paragraph
- `<h1>`-`<h6>`: Headings
- `<a>`: Anchor (link)
- `<img>`: Image
