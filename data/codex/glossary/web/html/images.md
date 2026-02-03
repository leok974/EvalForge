---
id: web/html/images
title: HTML Images
category: html
tags: [html, images, media]
---

# HTML Images

The `<img>` element embeds images in web pages.

## Basic Syntax

```html
<img src="path/to/image.jpg" alt="Description">
```

## Required Attributes

- **`src`**: Image source URL (required)
- **`alt`**: Alternative text for accessibility (required)

## Optional Attributes

- **`width`**, **`height`**: Dimensions in pixels
- **`loading`**: `lazy` for deferred loading
- **`srcset`**: Responsive images for different screen sizes

## Responsive Images

```html
<img 
  src="image-800.jpg" 
  srcset="image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w"
  sizes="(max-width: 600px) 400px, 800px"
  alt="Description">
```

## Best Practices

- **Always** include `alt` attribute
- Use descriptive alt text (not "image" or "photo")
- Specify dimensions to prevent layout shift
- Use appropriate file formats (JPEG, PNG, WebP, SVG)
- Optimize file sizes for performance

## Common Formats

- **JPEG**: Photos, complex images
- **PNG**: Transparency, graphics
- **SVG**: Logos, icons (scalable)
- **WebP**: Modern format, smaller sizes
