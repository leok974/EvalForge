---
id: web/html/metadata-seo
title: HTML Metadata and SEO
category: html
tags: [html, meta, seo, head]
---

# HTML Metadata and SEO

Metadata in the `<head>` section improves search engine optimization and user experience.

## Essential Meta Tags

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title - Site Name</title>
  <meta name="description" content="Brief page description (150-160 chars)">
</head>
```

## Viewport Meta Tag

Critical for responsive design:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

## Page Title

```html
<title>Specific Topic - Section - Site Name</title>
```

**Best practices:**
- 50-60 characters
- Most important keywords first
- Include brand name
- Unique for each page

## Meta Description

```html
<meta name="description" content="Compelling summary that appears in search results">
```

**Best practices:**
- 150-160 characters
- Include target keywords
- Call-to-action when appropriate
- Unique for each page

## Open Graph (Social Media)

```html
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Description">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">
```

## Twitter Cards

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Description">
<meta name="twitter:image" content="https://example.com/image.jpg">
```

## Other Useful Tags

```html
<meta name="robots" content="index, follow">
<meta name="author" content="Author Name">
<link rel="canonical" href="https://example.com/page">
<link rel="icon" href="/favicon.ico">
```

## Best Practices

- Include charset and viewport on every page
- Write unique titles and descriptions
- Optimize for both search engines and humans
- Test social media previews
- Keep metadata current and accurate
