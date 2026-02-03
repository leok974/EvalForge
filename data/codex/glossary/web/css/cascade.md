---
id: web/css/cascade
title: CSS Cascade
category: css
tags: [css, cascade, basics]
---

# CSS Cascade

The cascade determines which CSS rules apply when multiple rules target the same element.

## Cascade Order

CSS applies rules in this priority order (highest to lowest):

1. **Importance**: `!important` declarations
2. **Specificity**: More specific selectors win
3. **Source Order**: Last rule wins if specificity is equal

## Origins of Styles

Styles come from three sources (highest to lowest priority):

1. **Author styles**: Your CSS files
2. **User styles**: User browser preferences
3. **Browser defaults**: Default browser styles

## Example

```css
/* First rule */
p { color: blue; }

/* Second rule - wins due to source order */
p { color: red; }

/* Class selector - wins due to higher specificity */
.special { color: green; }

/* Important - wins but avoid using */
p { color: purple !important; }
```

## Inheritance vs Cascade

- **Cascade**: Resolves conflicts between rules
- **Inheritance**: Children inherit parent styles

## Best Practices

- Avoid `!important` (makes debugging harder)
- Understand specificity to predict which rules apply
- Organize CSS with consistent patterns
- Use source order intentionally
- Let cascade work for you, don't fight it
