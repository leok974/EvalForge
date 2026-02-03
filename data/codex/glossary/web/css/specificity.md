---
id: web/css/specificity
title: CSS Specificity
category: css
tags: [css, specificity, cascade]
---

# CSS Specificity

Specificity determines which CSS rules apply when multiple rules target the same element.

## Specificity Hierarchy

From highest to lowest:

1. **Inline styles**: `style="color: red"` (1000 points)
2. **IDs**: `#header` (100 points)
3. **Classes, attributes, pseudo-classes**: `.nav`, `[type="text"]`, `:hover` (10 points)
4. **Elements, pseudo-elements**: `div`, `::before` (1 point)

## Calculating Specificity

```css
/* 1 (div) */
div { }

/* 11 (div + class) */
div.container { }

/* 111 (ID + class + element) */
#header .nav li { }

/* 1 (element) */
p { }

/* 11 (class + pseudo-class) */
.button:hover { }
```

## Important Note

```css
p { color: blue !important; }
```

`!important` overrides all specificity but should be avoided.

## Specificity Rules

- More specific selectors win
- Equal specificity: last rule wins (source order)
- Inherited styles have no specificity

## Best Practices

- Keep specificity low and consistent
- Avoid `!important`
- Prefer classes over IDs
- Don't over-qualify selectors (`div.classname` → `.classname`)
- Use CSS methodologies (BEM, SMACSS) to manage specificity

## Debugging Tip

Use browser DevTools to see which rules apply and their specificity.
