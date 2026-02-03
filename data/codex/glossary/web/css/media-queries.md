---
id: web/css/media-queries
title: CSS Media Queries
category: css
tags: [css, media-queries, responsive]
---

# CSS Media Queries

Adapt styles based on device characteristics like screen size.

## Basic Syntax

```css
@media (min-width: 768px) {
  /* Styles for screens >= 768px */
  .container {
    max-width: 960px;
  }
}
```

## Common Breakpoints

```css
/* Mobile first approach */
/* Default: Mobile styles */

@media (min-width: 640px) {
  /* Tablet and up */
}

@media (min-width: 768px) {
  /* Desktop and up */
}

@media (min-width: 1024px) {
  /* Large desktop */
}

@media (min-width: 1280px) {
  /* Extra large */
}
```

## Media Features

### Width and Height

```css
@media (min-width: 768px) and (max-width: 1024px) {
  /* Tablet range */
}

@media (min-height: 600px) {
  /* Minimum viewport height */
}
```

### Orientation

```css
@media (orientation: portrait) {
  /* Vertical orientation */
}

@media (orientation: landscape) {
  /* Horizontal orientation */
}
```

### Display Mode

```css
@media (prefers-color-scheme: dark) {
  /* Dark mode */
  body { background: #1a1a1a; color: #fff; }
}

@media (prefers-reduced-motion: reduce) {
  /* Reduce animations for accessibility */
  * { animation: none !important; }
}
```

### Print

```css
@media print {
  /* Printer-friendly styles */
  nav, footer { display: none; }
  body { font-size: 12pt; }
}
```

## Combining Queries

```css
@media (min-width: 768px) and (orientation: landscape) {
  /* Desktop landscape */
}

@media screen and (min-width: 768px),
       print {
  /* Desktop OR print */
}
```

## Mobile-First vs Desktop-First

### Mobile-First (Recommended)

```css
/* Base: Mobile styles */
.container { width: 100%; }

/* Scale up */
@media (min-width: 768px) {
  .container { width: 750px; }
}
```

### Desktop-First

```css
/* Base: Desktop styles */
.container { width: 1200px; }

/* Scale down */
@media (max-width: 768px) {
  .container { width: 100%; }
}
```

## Container Queries

```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 1fr 2fr;
  }
}
```

## Best Practices

- Use mobile-first approach (`min-width`)
- Keep breakpoint count minimal (3-4)
- Base breakpoints on content, not devices
- Test on real devices
- Use relative units (`em`, `rem`) in media queries
- Consider `prefers-reduced-motion` for accessibility

## Common Patterns

```css
/* Responsive navigation */
.nav {
  display: none;  /* Hidden on mobile */
}

@media (min-width: 768px) {
  .nav { display: flex; }
  .menu-toggle { display: none; }
}

/* Responsive grid */
.grid {
  display: grid;
  gap: 1rem;
}

@media (min-width: 640px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}
```
