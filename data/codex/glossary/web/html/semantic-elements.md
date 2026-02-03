---
id: web/html/semantic-elements
title: HTML Semantic Elements
category: html
tags: [html, semantic, structure, accessibility]
---

# HTML Semantic Elements

Semantic elements clearly describe their meaning to browsers and developers.

## Page Structure

```html
<header>
  <nav>
    <!-- Navigation links -->
  </nav>
</header>

<main>
  <article>
    <section>
      <h2>Section heading</h2>
      <p>Content...</p>
    </section>
  </article>
  
  <aside>
    <!-- Sidebar content -->
  </aside>
</main>

<footer>
  <!-- Footer content -->
</footer>
```

## Key Elements

- **`<header>`**: Introductory content, logo, nav
- **`<nav>`**: Navigation links
- **`<main>`**: Primary content (one per page)
- **`<article>`**: Self-contained content
- **`<section>`**: Thematic grouping
- **`<aside>`**: Tangentially related content
- **`<footer>`**: Footer information

## Content Elements

- **`<figure>`** / **`<figcaption>`**: Images with captions
- **`<time>`**: Dates and times
- **`<mark>`**: Highlighted text
- **`<details>`** / **`<summary>`**: Collapsible content

## Benefits

✅ **SEO**: Better search engine understanding  
✅ **Accessibility**: Screen readers navigate better  
✅ **Maintainability**: Clear code structure  
✅ **Consistency**: Standard patterns

## Avoid


❌ **Don't use:** `<div>` and `<span>` for everything  
✅ **Instead:** Choose semantic elements that match content purpose

## Best Practices

- Use one `<main>` per page
- Nest sections logically
- Add ARIA labels when needed
- Structure content hierarchically
