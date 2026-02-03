# Positioning & Z-Index: Layer With Confidence

## Outcome

In this quest, you'll master CSS positioning (static, relative, absolute, fixed, sticky) and z-index to precisely place elements, create layered interfaces, and build modals, tooltips, and fixed headers without mystery overlaps.

## Concept in 30 seconds

Elements are positioned **static** by default (normal flow). **Relative** positions offset from normal position. **Absolute** positions relative to nearest positioned ancestor. **Fixed** positions relative to viewport. **Sticky** toggles between relative and fixed. **Z-index** controls stacking order of positioned elements.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/css-position-zindex/terms.json) and linked to the Codex:

- **position** - CSS property controlling element placement method
- **relative** - Positioned relative to normal position
- **absolute** - Positioned relative to nearest positioned ancestor
- **fixed** - Positioned relative to viewport
- **z-index** - Controls stacking order of overlapping elements
- **stacking context** - 3D layer context created by positioned elements

## Walkthrough

1. **Understand positioning contexts**: Static → normal flow, others create contexts
2. **Use relative for offsets**: Nudge elements without affecting layout
3. **Absolute for precise placement**: Position within nearest positioned parent
4. **Fixed for persistent UI**: Headers, modals that stay during scroll
5. **Sticky for hybrid behavior**: Scroll-then-stick navigation
6. **Manage z-index**: Higher values appear in front

## Example implementation

```css
/* Static (default) - normal document flow */
.normal {
  position: static;  /* Default, rarely specified */
}

/* Relative - offset from normal position */
.nudged {
  position: relative;
  top: 10px;   /* Push down 10px from where it would be */
  left: 20px;  /* Push right 20px */
  /* Still occupies original space in layout */
}

/* Absolute - positioned within parent */
.parent {
  position: relative;  /* Establishes positioning context */
}

.badge {
  position: absolute;
  top: -10px;
  right: -10px;
  z-index: 1;  /* Above parent */
}

/* Fixed - viewport relative */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;  /* Above page content */
}

/* Sticky - switches between relative and fixed */
.sticky-nav {
  position: sticky;
  top: 0;  /* Sticks at top when scrolled to */
  z-index: 10;
}

/* Modal overlay (common pattern) */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.modal-content {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);  /* Center */
  z-index: 1001;  /* Above overlay */
}

/* Tooltip */
.tooltip-trigger {
  position: relative;
}

.tooltip {
  position: absolute;
  bottom: 100%;  /* Above trigger */
  left: 50%;
  transform: translateX(-50%);  /* Horizontal center */
  z-index: 999;
}

/* Stacking context example */
.context-1 {
  position: relative;
  z-index: 1;
}

.context-1-child {
  position: relative;
  z-index: 9999;  /* Can't escape parent context */
}

.context-2 {
  position: relative;
  z-index: 2;  /* Appears above entire context-1 group */
}
```

**Position values:**
- `static` - Default, not positioned
- `relative` - Offset from normal position
- `absolute` - Positioned within containing block
- `fixed` - Positioned within viewport
- `sticky` - Relative until scroll threshold, then fixed

**Z-index rules:**
- Only works on positioned elements (not static)
- Higher z-index = closer to viewer
- Siblings with same z-index: source order decides
- Each stacking context is independent

## Common mistakes

- **z-index without position**: Doesn't work on `position: static`
- **z-index wars**: Using `z-index: 999999` instead of understanding context
- **Forgetting positioning context**: Absolute element escapes to `<body>`
- **Fixed on mobile**: Can cover content, test thoroughly
- **Not accounting for removed layout space**: Absolute/fixed removes element from flow

## Deep dive

When you set `position: absolute`, the element positions relative to its **nearest positioned ancestor** (any position except `static`). If no ancestor is positioned, it uses `<body>`. The common pattern is `position: relative` on parent (no offset) purely to establish the context for absolute children.

Stacking contexts create isolated 3D layers. When an element creates a stacking context (via `position` + `z-index`, `opacity < 1`, `transform`, etc.), its children stack together, independent of external elements. Even if child has `z-index: 9999`, it can't escape its parent's context.This prevents z-index arms races.

The `position: sticky` value is relative positioning until a scroll threshold is reached(`top: 0` means "when element scrolls to top of viewport"), then it becomes fixed until its container scrolls past. This creates the "scroll-then-stick" navigation pattern without JavaScript.

The transform `translate(-50%, -50%)` centering trick positions an element's top-left at 50% viewport, then shifts it back by half its own width/height, perfectly centering it regardless of size. Combine with `position: fixed` for modals.

Z-index doesn't need huge numbers. A sensible scale: 0-9 for normal content, 10-99 for dropdowns/tooltips, 100-999 for modals/overlays, 1000+ for extreme cases like cookie banners. Document your z-index scale in comments.
