---
id: web/css/flexbox
title: CSS Flexbox
category: css
tags: [css, flexbox, layout]
---

# CSS Flexbox

Flexible box layout for one-dimensional layouts (row or column).

## Basic Setup

```css
.container {
  display: flex;
}
```

## Container Properties

### Direction

```css
.container {
  flex-direction: row;           /* default */
  flex-direction: row-reverse;
  flex-direction: column;
  flex-direction: column-reverse;
}
```

### Wrapping

```css
.container {
  flex-wrap: nowrap;    /* default, single line */
  flex-wrap: wrap;      /* multi-line */
  flex-wrap: wrap-reverse;
}
```

### Justify Content (Main Axis)

```css
.container {
  justify-content: flex-start;    /* default */
  justify-content: flex-end;
  justify-content: center;
  justify-content: space-between; /* Even spacing between items */
  justify-content: space-around;  /* Even spacing around items */
  justify-content: space-evenly;  /* Equal spacing */
}
```

### Align Items (Cross Axis)

```css
.container {
  align-items: stretch;      /* default */
  align-items: flex-start;
  align-items: flex-end;
  align-items: center;
  align-items: baseline;
}
```

### Align Content (Multi-line)

```css
.container {
  flex-wrap: wrap;
  align-content: flex-start;
  align-content: center;
  align-content: space-between;
}
```

## Item Properties

### Flex Grow

```css
.item {
  flex-grow: 1;  /* Take available space */
}
```

### Flex Shrink

```css
.item {
  flex-shrink: 1;  /* Allow shrinking (default) */
  flex-shrink: 0;  /* Never shrink */
}
```

### Flex Basis

```css
.item {
  flex-basis: 200px;  /* Starting size */
  flex-basis: auto;   /* default */
}
```

### Flex Shorthand

```css
.item {
  flex: 1;              /* grow shrink basis */
  flex: 1 0 200px;      /* Common: grow to fill, don't shrink below 200px */
}
```

### Align Self

```css
.item {
  align-self: auto;       /* default */
  align-self: flex-start;
  align-self: center;
  align-self: flex-end;
}
```

### Order

```css
.item {
  order: 0;   /* default */
  order: 1;   /* Appears later */
  order: -1;  /* Appears first */
}
```

## Common Patterns

```css
/* Center everything */
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Equal-width columns */
.columns {
  display: flex;
}
.column {
  flex: 1;
}

/* Navigation bar */
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Card grid */
.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
.card {
  flex: 1 1 300px;  /* grow, shrink, min-width */
}
```

## Gap Property

```css
.container {
  display: flex;
  gap: 1rem;          /* Spacing between items */
  row-gap: 1rem;
  column-gap: 2rem;
}
```

## Best Practices

- Use for one-dimensional layouts
- Combine with Grid for complex layouts
- Use `gap` instead of margins when possible
- Understand main axis vs cross axis
- Use `flex: 1` for equal-width children
