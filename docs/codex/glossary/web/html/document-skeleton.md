---
id: glossary/web/html/document-skeleton
title: Document Skeleton
world: web
level: beginner
tags: [html, structure, fundamentals]
related:
  - codex:glossary/web/html/metadata-seo
  - codex:glossary/web/html/semantic-elements
  - codex:glossary/web/html/tags-and-elements
---

# Document Skeleton

## Definition
The document skeleton is the minimal structure of an HTML page: doctype, `<html>`, `<head>`, and `<body>`. The head contains metadata; the body contains visible content.

## Usage
- Set title + meta tags in `<head>`.
- Load CSS/JS safely (defer scripts when possible).
- Keep semantic structure inside `<body>`.

## Example
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>My Page</title>
  </head>
  <body>
    <main>Hello</main>
  </body>
</html>
```

## Pitfalls

* Missing viewport breaks mobile scaling.
* Putting visible content in `<head>` won't render properly.

## Related

* Metadata Seo: meta tags go in the document head.
* Semantic Elements: body contains semantic structure.
* Tags And Elements: skeleton is built from tags/elements.