---
id: glossary/web/html/links
title: Links
world: web
level: beginner
tags: [html, navigation, seo]
related:
  - codex:glossary/web/html/metadata-seo
  - codex:glossary/web/html/semantic-elements
---

# Links

## Definition
Links connect pages/resources using `<a href="...">`. They can be internal routes, external sites, or file downloads, and can include security-related attributes.

## Usage
- Use meaningful link text (not "click here").
- Add `rel="noopener noreferrer"` for external `target="_blank"`.
- Use anchors (`#section`) for page navigation.

## Example
```html
<a href="https://example.com" target="_blank" rel="noopener noreferrer">
  Open docs
</a>
```

## Pitfalls

* `target="_blank"` without `noopener` can be a security risk.
* Styling links without hover/focus states hurts UX.

## Related

* Metadata Seo: links affect SEO and crawling.
* Semantic Elements: navigation uses semantic nav elements.