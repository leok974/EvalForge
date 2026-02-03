# Grid Layout: Two-Dimensional Control

## Outcome

In this quest, you'll master CSS Grid for two-dimensional layouts—defining columns and rows, placing items precisely, and using grid areas for complex page structures that adapt fluidly without fragile positioning.

## Concept in 30 seconds

Grid creates a two-dimensional layout system with explicit rows and columns. Define tracks with `grid-template-columns` and `grid-template-rows`, use the `fr` unit for flexible sizing, and place items with `grid-area` or line numbers. Grid excels at page-level layouts.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/css-grid/terms.json) and linked to the Codex:

- **grid container** - Parent element with display: grid
- **grid template columns** - Defines column structure and sizes
- **fr unit** - Fraction of available space for flexible sizing
- **grid area** - Named region in grid template
- **gap** - Spacing between grid cells

## Walkthrough

1. **Create grid container**: `display: grid` on parent
2. **Define columns**: `grid-template-columns: 1fr 2fr 1fr` for 3 columns
3. **Set rows**: `grid-template-rows: auto 1fr auto` for header/content/footer
4. **Add gap**: `gap: 20px` for gutters
5. **Place items**: Use `grid-column` / `grid-row` or `grid-area`
6. **Make responsive**: Use `minmax()`, `repeat()`, and `auto-fit`

## Example implementation

```css
/* Basic grid */
.grid-container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;  /* 3 equal columns */
  gap: 20px;
}

/* Holy Grail layout (named areas) */
.layout {
  display: grid;
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header header header"
    "sidebar main aside"
    "footer footer footer";
  gap: 1rem;
  min-height: 100vh;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }

/* Responsive card grid (auto-fit) */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

/* Dashboard layout */
.dashboard {
  display: grid;
  grid-template-columns: repeat(12, 1fr);  /* 12-column system */
  gap: 1rem;
}

.widget-large {
  grid-column: span 8;   /* Takes 8 columns */
}

.widget-small {
  grid-column: span 4;   /* Takes 4 columns */
}

/* Explicit placement */
.featured {
  grid-column: 1 / 3;    /* From line 1 to 3 */
  grid-row: 1 / 3;       /* Span 2 rows */
}

/* Dense packing */
.masonry {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-auto-flow: dense;  /* Fill gaps with smaller items */
}
```

**Grid container properties:**
- `grid-template-columns/rows`: Define track sizes
- `grid-template-areas`: Named layout regions
- `gap`: Spacing between cells
- `justify-items` / `align-items`: Align all items
- `grid-auto-flow`: Control automatic placement

**Grid item properties:**
- `grid-column` / `grid-row`: Line-based placement
- `grid-area`: Named area placement
- `justify-self` / `align-self`: Individual alignment

**Useful functions:**
- `fr` - Flexible fraction of space
- `repeat(n, size)` - Repeat pattern n times
- `minmax(min, max)` - Clamp size between values
- `auto-fit` / `auto-fill` - Responsive columns

## Common mistakes

- **Forgetting fr units**: Using percentages instead of flexible fractions
- **Not using minmax**: Fixed sizes break on small screens
- **Over-specifying placement**:  Let auto-placement work when possible
- **Missing gap**: Items touch, looks cramped
- **Confusing auto-fit vs auto-fill**: `auto-fit` collapses empty tracks, `auto-fill` doesn't

## Deep dive

The `fr` unit distributes **remaining space** after fixed-size tracks. With `grid-template-columns: 200px 1fr 2fr`, the 200px is allocated first, then remaining space divides 1:2 between the other columns.

`repeat(auto-fit, minmax(300px, 1fr))` creates responsive grids without media queries. It places as many 300px-minimum columns as fit, then expands them to fill space. `auto-fit` collapses empty tracks, so 3 cards expand fully if there's room for 5. `auto-fill` keeps empty tracks, preventing excessive expansion.

Named grid areas create readable templates. The ASCII-art layout in `grid-template-areas` visually represents the grid structure. This beats line numbers for maintainability—you see the layout shape in the CSS.

Grid's auto-placement algorithm fills tracks sequentially unless you specify `grid-auto-flow: dense`, which backtracks to fill gaps with smaller items. This creates tighter layouts but changes source order visually, which can harm accessibility.

Placing items using line numbers counts from track lines, not cells: `grid-column: 1 / 3` spans from the first line to the third, covering two cells. Negative numbers count from the end: `grid-column: 1 / -1` spans the full width.

Grid and Flexbox aren't rivals—they complement each other. Use Grid for page-level structure (multi-dimensional), Flexbox for component layout (one-dimensional). It's common to have a Grid page layout with Flexbox navigation bars and card interiors.

## Check yourself

Before moving on, verify you can:
- Explain the core concepts covered in this quest
- Identify common mistakes and how to avoid them
- Apply the techniques in your own projects
- Debug issues when things don't work as expected

