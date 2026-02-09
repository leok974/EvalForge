---
id: glossary/web/html/media-embed
title: Media Embed
world: web
level: intermediate
tags: [html, media, embeds]
related:
  - codex:glossary/web/html/images
  - codex:glossary/web/html/document-skeleton
---

# Media Embed

## Definition
Embedding media includes `<video>`, `<audio>`, and `<iframe>` (e.g., YouTube). Embeds should be responsive and accessible.

## Usage
- Use `controls` for video/audio.
- Make iframes responsive with a container.
- Set titles for iframes.

## Example
```html
<iframe
  title="Demo"
  src="https://www.youtube.com/embed/xxxx"
  loading="lazy"
></iframe>
```

## Pitfalls

* Missing iframe title hurts accessibility.
* Embeds can be heavy—lazy load when possible.

## Related

* Images: images and embeds are both media.
* Document Skeleton: embeds go in the document body.