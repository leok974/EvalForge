---
id: web/html/tables
title: HTML Tables
category: html
tags: [html, tables, data]
---

# HTML Tables

Tables display tabular data in rows and columns.

## Basic Structure

```html
<table>
  <thead>
    <tr>
      <th>Header 1</th>
      <th>Header 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Data 1</td>
      <td>Data 2</td>
    </tr>
  </tbody>
</table>
```

## Key Elements

- **`<table>`**: Container
- **`<thead>`**: Header section
- **`<tbody>`**: Body content
- **`<tfoot>`**: Footer section
- **`<tr>`**: Table row
- **`<th>`**: Header cell (bold, centered)
- **`<td>`**: Data cell

## Spanning Cells

```html
<td colspan="2">Spans 2 columns</td>
<td rowspan="3">Spans 3 rows</td>
```

## Accessibility

```html
<table>
  <caption>Monthly Sales Report</caption>
  <thead>
    <tr>
      <th scope="col">Month</th>
      <th scope="col">Sales</th>
    </tr>
  </thead>
</table>
```

## When to Use Tables

✅ **Use for:** Tabular data, comparisons, schedules  
❌ **Don't use for:** Page layout, navigation, styling

## Best Practices

- Include `<caption>` for table description
- Use `<th scope="">` for accessibility
- Structure with `<thead>`, `<tbody>`, `<tfoot>`
- Never use tables for layout
