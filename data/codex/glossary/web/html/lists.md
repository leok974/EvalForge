---
id: web/html/lists
title: HTML Lists
category: html
tags: [html, lists, structure]
---

# HTML Lists

HTML provides three types of lists for organizing content.

## Unordered Lists

For items without specific order:

```html
<ul>
  <li>First item</li>
  <li>Second item</li>
  <li>Third item</li>
</ul>
```

## Ordered Lists

For sequential items:

```html
<ol>
  <li>Step one</li>
  <li>Step two</li>
  <li>Step three</li>
</ol>
```

## Description Lists

For term-definition pairs:

```html
<dl>
  <dt>Term</dt>
  <dd>Definition of the term</dd>
  <dt>Another term</dt>
  <dd>Another definition</dd>
</dl>
```

## Nested Lists

```html
<ul>
  <li>Parent item
    <ul>
      <li>Child item</li>
      <li>Child item</li>
    </ul>
  </li>
  <li>Parent item</li>
</ul>
```

## Best Practices

- Use `<ul>` for unordered collections
- Use `<ol>` for procedural steps or rankings
- Use `<dl>` for glossaries or metadata
- Keep list items concise and parallel in structure
