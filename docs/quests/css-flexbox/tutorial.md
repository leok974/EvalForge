# Flexbox Layout: Align and Distribute

## Outcome

In this quest, you'll master Flexbox for one-dimensional layouts—controlling alignment, distribution, and ordering of items along a main axis—building responsive components without float hacks or precise calculations.

## Concept in 30 seconds

Flexbox operates on a **flex container** (parent with `display: flex`) and **flex items** (direct children). Control main-axis distribution with `justify-content`, cross-axis alignment with `align-items`, and use `gap` for spacing. Items can grow, shrink, and wrap automatically.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/css-flexbox/terms.json) and linked to the Codex:

- **flex container** - Parent element with display: flex
- **flex item** - Direct child of flex container
- **justify-content** - Aligns items along main axis
- **align-items** - Aligns items along cross axis
- **gap** - Spacing between flex items

## Walkthrough

1. **Create flex container**: `display: flex` on parent
2. **Set direction**: `flex-direction: row` (default) or `column`
3. **Align main axis**: `justify-content: space-between`, `center`, etc.
4. **Align cross axis**: `align-items: center`, `flex-start`, etc.
5. **Add spacing**: `gap: 20px` between items
6. **Control wrapping**: `flex-wrap: wrap` for responsive layouts

## Example implementation

```css
/* Basic flex container */
.flex-container {
  display: flex;
  gap: 20px;           /* Spacing between items */
}

/* Navigation bar (horizontal) */
.navbar {
  display: flex;
  justify-content: space-between;  /* Space items apart */
  align-items: center;             /* Vertically center */
  padding: 1rem;
}

/* Centered content */
.center-box {
  display: flex;
  justify-content: center;  /* Horizontal center */
  align-items: center;      /* Vertical center */
  min-height: 100vh;        /* Full viewport height */
}

/* Equal-width columns */
.columns {
  display: flex;
  gap: 2rem;
}

.columns > * {
  flex: 1;  /* Equal distribution */
}

/* Responsive card layout */
.card-grid {
  display: flex;
  flex-wrap: wrap;     /* Wrap to new rows */
  gap: 1.5rem;
}

.card {
  flex: 1 1 300px;     /* Grow, shrink, min-width 300px */
}

/* Column layout */
.sidebar-layout {
  display: flex;
}

.sidebar {
  flex: 0 0 250px;     /* Fixed 250px width */
}

.main-content {
  flex: 1;             /* Fill remaining space */
}

/* Reversing order */
.reverse {
  flex-direction: row-reverse;  /* Right to left */
}

/* Individual item alignment */
.flex-container .special-item {
  align-self: flex-end;  /* Different alignment than siblings */
}
```

**Flex container properties:**
- `flex-direction`: row | column | row-reverse | column-reverse
- `justify-content`: flex-start | center | space-between | space-around | space-evenly
- `align-items`: flex-start | center | flex-end | stretch | baseline
- `flex-wrap`: nowrap | wrap | wrap-reverse
- `gap`: spacing between items

**Flex item properties:**
- `flex-grow`: grow factor (default 0)
- `flex-shrink`: shrink factor (default 1)
- `flex-basis`: initial size
- `flex`: shorthand (grow shrink basis)
- `align-self`: override container's align-items

## Common mistakes

- **Not using gap**: Adding margins to flex items instead of `gap` on container
- **Forgetting flex-wrap**: Items squeeze instead of wrapping to new lines
- **Wrong axis**: Confusing justify-content (main) with align-items (cross)
- **Not setting flex-basis**: `flex: 1` without minimum size causes squishing
- **Nested flex confusion**: Inner flex contexts are independent

## Deep dive

The `flex` shorthand combines three properties: `flex: <grow> <shrink> <basis>`. Common patterns:
- `flex: 1` → `1 1 0` (equal distribution, can grow/shrink from zero)
- `flex: 0 0 200px` → Fixed 200px width, no grow/shrink
- `flex: 1 1 300px` → Can grow/shrink, but starts at 300px minimum

The gap property is superior to margins for flex spacing because it only adds space **between** items, not before the first or after the last. Compare `gap: 20px` vs `> * { margin-right: 20px; last-child { margin-right: 0; } }`.

Flexbox's main axis follows `flex-direction`: horizontal for `row`, vertical for `column`. The cross axis is perpendicular. `justify-content` always aligns along the main axis, `align-items` along the cross axis. Switching to `flex-direction: column` rotates this entire coordinate system.

The `align-self` property overrides the container's `align-items` for individual items. Use it when one item needs different cross-axis alignment than its siblings, like a callout button aligned to the bottom while text is centered.

## Check yourself

Before moving on, verify you can:
- Explain the core concepts covered in this quest
- Identify common mistakes and how to avoid them
- Apply the techniques in your own projects
- Debug issues when things don't work as expected

