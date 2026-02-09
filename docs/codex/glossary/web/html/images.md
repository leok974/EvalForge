---
id: glossary/web/html/images
title: Images
world: web
level: beginner
tags: [html, media, assets]
related:
  - codex:glossary/web/html/attributes
  - codex:glossary/web/css/backgrounds
---

# Images

## Definition
Images are embedded with `<img>` or via CSS backgrounds. Use `alt` text for meaning and responsive sizing to avoid layout shifts.

## Usage
- Always provide `alt`.
- Set width/height to reduce CLS.
- Use `max-width: 100%` for responsiveness.

## Example
```html
<img src="/banner.jpg" alt="Orion map overview" width="1200" height="630" />
```

## Pitfalls

* Missing dimensions can cause layout jumps.
* Huge images without compression slow pages.

## Related

* Attributes: images use alt and size attributes.
* Backgrounds: CSS backgrounds are an alternative to img elements.