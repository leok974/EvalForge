---
id: web/css/grid
title: CSS Grid
category: css
tags: [css, grid, layout]
---

# CSS Grid

Two-dimensional layout system for rows and columns.

## Basic Setup

```css
.container {
  display: grid;
  grid-template-columns: 200px 1fr 200px;  /* 3 columns */
  grid-template-rows: auto 1fr auto;       /* 3 rows */
  gap: 1rem;
}
```

## Defining Columns and Rows

```css
.grid {
  /* Fixed widths */
  grid-template-columns: 200px 400px 200px;
  
  /* Flexible units */
  grid-template-columns: 1fr 2fr 1fr;
  
  /* Repeat */
  grid-template-columns: repeat(3, 1fr);
  
  /* Auto-fill responsive */
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  
  /* Named lines */
  grid-template-columns: [sidebar-start] 200px [sidebar-end main-start] 1fr [main-end];
}
```

## Grid Units

- **`fr`**: Fraction of available space
- **`auto`**: Size based on content
- **`minmax(min, max)`**: Range of sizes
- **`min-content`**, **`max-content`**: Content-based sizing

## Gap

```css
.grid {
  gap: 1rem;              /* row and column */
  row-gap: 1rem;
  column-gap: 2rem;
}
```

## Placing Items

```css
.item {
  /* By line numbers */
  grid-column: 1 / 3;     /* Span columns 1-3 */
  grid-row: 1 / 2;
  
  /* Span keyword */
  grid-column: span 2;     /* Span 2 columns */
  
  /* Named areas */
  grid-area: header;
}
```

## Grid Template Areas

```css
.container {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main main"
    "footer footer footer";
  grid-template-columns: 200px 1fr 1fr;
  grid-template-rows: auto 1fr auto;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

## Alignment

### Container Alignment

```css
.container {
  /* Align all items */
  justify-items: start;    /* horizontal */
  align-items: start;      /* vertical */
  
  /* Align grid within container */
  justify-content: center;
  align-content: center;
}
```

### Item Alignment

```css
.item {
  justify-self: center;    /* horizontal */
  align-self: center;      /* vertical */
}
```

## Auto-Placement

```css
.grid {
  grid-auto-flow: row;      /* default */
  grid-auto-flow: column;
  grid-auto-flow: dense;    /* Fill gaps */
  
  grid-auto-rows: 100px;    /* Size of auto rows */
  grid-auto-columns: 100px;
}
```

## Common Patterns

```css
/* Responsive card grid */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

/* Holy Grail Layout */
.layout {
  display: grid;
  grid-template-areas:
    "header header header"
    "nav main aside"
    "footer footer footer";
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

/* Full-bleed images */
.article {
  display: grid;
  grid-template-columns: 1fr min(60ch, 100%) 1fr;
}
.content { grid-column: 2; }
.full-width { grid-column: 1 / -1; }
```

## Best Practices

- Use for two-dimensional layouts
- Combine with Flexbox for best results
- Use `fr` units for flexible columns
- Use `repeat(auto-fit, minmax())` for responsive grids
- Name areas for clarity in complex layouts
- Use gap instead of margins
