---
id: web/html/accessibility-basics
title: HTML Accessibility Basics
category: html
tags: [html, accessibility, a11y, wcag]
---

# HTML Accessibility Basics

Making web content usable for everyone, including people with disabilities.

## Core Principles

1. **Perceivable**: Content must be presentable to users
2. **Operable**: Interface must be navigable
3. **Understandable**: Information must be clear
4. **Robust**: Content works across technologies

## Essential Practices

### Alternative Text

```html
<img src="chart.png" alt="Sales increased 25% in Q4">
```

### Labels for Form Inputs

```html
<label for="email">Email Address:</label>
<input type="email" id="email" name="email">
```

### Semantic HTML

```html
<!-- Good -->
<button type="submit">Submit</button>

<!-- Bad -->
<div onclick="submit()">Submit</div>
```

### Keyboard Navigation

- All interactive elements must be keyboard-accessible
- Use proper tab order
- Provide visible focus indicators

### ARIA Labels

```html
<nav aria-label="Primary navigation">
  <!-- Links -->
</nav>

<button aria-label="Close dialog">×</button>
```

## Landmarks

Use semantic elements for screen reader navigation:

```html
<header role="banner">
<nav role="navigation">
<main role="main">
<aside role="complementary">
<footer role="contentinfo">
```

## Heading Hierarchy

```html
<h1>Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>
  <h2>Another Section</h2>
```

## Best Practices

- Use semantic HTML first
- Add ARIA only when HTML isn't enough
- Test with keyboard navigation
- Test with screen readers
- Ensure sufficient color contrast (4.5:1 minimum)
- Provide captions for videos
- Don't rely on color alone to convey information
