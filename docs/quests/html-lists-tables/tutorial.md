# Lists & Tables: Organize Information

## Outcome

In this quest, you'll structure content using lists (ul, ol, dl) and tables, understanding when to use each type and how to make tabular data accessible with proper semantic markup.

## Concept in 30 seconds

Lists organize related items—use `<ul>` when order doesn't matter, `<ol>` when it does, and `<dl>` for term-definition pairs. Tables display grid data with rows and columns, using `<thead>`, `<tbody>`, and `scope` attributes for accessibility.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/html-lists-tables/terms.json) and linked to the Codex:

- **unordered list** - Bulleted list where item order doesn't matter
- **ordered list** - Numbered list where sequence is meaningful
- **list item** - Individual entry within a list
- **table header** - Column/row header cell semantically identified
- **table row** - Horizontal row of table cells

## Walkthrough

1. **Choose list type**: ul for features, ol for steps, dl for glossaries
2. **Nest lists**: Place entire `<ul>`/`<ol>` inside a parent `<li>`
3. **Build table structure**: `<table>` → `<thead>` + `<tbody>` → `<tr>` → `<th>`/`<td>`
4. **Add scope attributes**: `<th scope="col">` or `scope="row"` for headers
5. **Use captions**: `<caption>` describes table purpose
6. **Avoid layout tables**: Tables are for data, not page layout

## Example implementation

```html
<!-- Unordered list -->
<ul>
  <li>Fast performance</li>
  <li>Easy to learn</li>
  <li>Great community</li>
</ul>

<!-- Ordered list with nesting -->
<ol>
  <li>Mix dry ingredients
    <ul>
      <li>2 cups flour</li>
      <li>1 tsp baking powder</li>
    </ul>
  </li>
  <li>Add wet ingredients</li>
  <li>Bake at 350°F for 25 minutes</li>
</ol>

<!-- Accessible data table -->
<table>
  <caption>Monthly Sales Report</caption>
  <thead>
    <tr>
      <th scope="col">Product</th>
      <th scope="col">Units Sold</th>
      <th scope="col">Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Widget A</th>
      <td>1,234</td>
      <td>$12,340</td>
    </tr>
    <tr>
      <th scope="row">Widget B</th>
      <td>892</td>
      <td>$8,920</td>
    </tr>
  </tbody>
</table>
```

## Common mistakes

- **Using `<br>` instead of lists**: Creates visual separation but no semantic meaning
- **Tables for layout**: Use CSS Grid/Flexbox instead—tables are for tabular data only
- **Missing `<thead>`/`<tbody>`**: Makes tables less accessible to screen readers
- **No `scope` on headers**: Screen readers can't associate headers with data cells
- **Improper nesting**: Putting `<ul>` directly inside `<ul>` instead of inside `<li>`

## Deep dive

List semantics matter for assistive technology. When a screen reader encounters a list, it announces "List, 5 items" before reading items, helping users mentally prepare. Nested lists create hierarchical relationships—screen readers announce depth level so users understand structure.

The `scope` attribute on `<th>` tells screen readers whether a header applies to a column (`scope="col"`) or row (`scope="row"`). Without this, screen readers reading cell "892" might not know it's "Widget B's Units Sold." For complex tables with multi-level headers, use `headers` and `id` attributes to explicitly associate cells with headers.


## Check yourself

Before moving on, verify you can:
- Explain the core concepts covered in this quest
- Identify common mistakes and how to avoid them
- Apply the techniques in your own projects
- Debug issues when things don't work as expected

