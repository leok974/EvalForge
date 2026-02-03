---
id: web/css/box-model
title: CSS Box Model
category: css
tags: [css, box-model, layout]
---

# CSS Box Model

Every element is a rectangular box with content, padding, border, and margin.

## Box Model Layers

From inside out:

1. **Content**: The actual content (text, images)
2. **Padding**: Space between content and border
3. **Border**: Border around padding
4. **Margin**: Space outside border (separates from other elements)

```
+---------------------------+
|        Margin             |
|  +---------------------+  |
|  |     Border          |  |
|  |  +---------------+  |  |
|  |  |   Padding     |  |  |
|  |  |  +---------+  |  |  |
|  |  |  | Content |  |  |  |
|  |  |  +---------+  |  |  |
|  |  +---------------+  |  |
|  +---------------------+  |
+---------------------------+
```

## Syntax

```css
.box {
  /* Individual sides */
  padding-top: 10px;
  padding-right: 20px;
  padding-bottom: 10px;
  padding-left: 20px;
  
  /* Shorthand: top right bottom left (clockwise) */
  padding: 10px 20px 10px 20px;
  
  /* Shorthand: vertical horizontal */
  padding: 10px 20px;
  
  /* All sides */
  padding: 10px;
}
```

## Box Sizing

```css
/* Default: width/height applies to content only */
.content-box {
  box-sizing: content-box;
  width: 200px;
  padding: 20px;
  /* Total width: 240px (200 + 20 + 20) */
}

/* Modern: width/height includes padding and border */
.border-box {
  box-sizing: border-box;
  width: 200px;
  padding: 20px;
  /* Total width: 200px (padding included) */
}
```

## Global Box Sizing Reset

```css
*, *::before, *::after {
  box-sizing: border-box;
}
```

## Margin Collapse

Vertical margins between adjacent elements collapse:

```css
.box1 { margin-bottom: 20px; }
.box2 { margin-top: 30px; }
/* Gap between boxes: 30px (not 50px) */
```

## Best Practices

- Use `box-sizing: border-box` globally
- Understand total element size = content + padding + border (+ margin for spacing)
- Use margin for spacing between elements
- Use padding for spacing inside elements
