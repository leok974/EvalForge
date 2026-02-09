---
id: glossary/web/html/metadata-seo
title: Metadata Seo
world: web
level: beginner
tags: [html, seo, meta-tags]
related:
  - codex:glossary/web/html/document-skeleton
  - codex:glossary/web/html/links
---

# Metadata Seo

## Definition
SEO metadata helps browsers and crawlers understand your page. Key items include `<title>`, meta description, canonical URLs, and social preview tags (Open Graph).

## Usage
- Set unique titles per page.
- Add description for search previews.
- Use OG tags for share cards.

## Example
```html
<title>EvalForge — Workshop</title>
<meta name="description" content="Practice quests with instant feedback." />
<meta property="og:title" content="EvalForge — Workshop" />
```

## Pitfalls

* Duplicate titles/descriptions reduce clarity in search results.
* Missing canonical URLs can create duplicate indexing issues.

## Related

* Document Skeleton: metadata lives in the document head.
* Links: canonical links prevent duplicate content.