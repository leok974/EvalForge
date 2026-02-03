---
id: web/css/selectors
title: CSS Selectors
category: css
tags: [css, selectors, basics]
---

# CSS Selectors

Selectors target HTML elements for styling.

## Basic Selectors

```css
/* Element selector */
p { color: blue; }

/* Class selector */
.highlight { background: yellow; }

/* ID selector */
#header { font-size: 24px; }

/* Universal selector */
* { margin: 0; }
```

## Combinators

```css
/* Descendant */
div p { }  /* All p inside div */

/* Child */
div > p { }  /* Direct p children of div */

/* Adjacent sibling */
h1 + p { }  /* p immediately after h1 */

/*General sibling */
h1 ~ p { }  /* All p siblings after h1 */
```

## Attribute Selectors

```css
[type="text"] { }
[href^="https"] { }  /* Starts with */
[href$=".pdf"] { }   /* Ends with */
[class*="btn"] { }   /* Contains */
```

## Pseudo-classes

```css
a:hover { }
a:visited { }
input:focus { }
li:first-child { }
li:nth-child(2n) { }  /* Even items */
```

## Pseudo-elements

```css
p::before { content: "→ "; }
p::after { content: " ←"; }
p::first-line { font-weight: bold; }
```

## Best Practices

- Prefer classes over IDs for styling
- Keep specificity low
- Use semantic class names
- Avoid over-qualifying selectors
