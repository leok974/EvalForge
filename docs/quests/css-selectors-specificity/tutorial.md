# Selectors & Specificity: Target Precisely

## Outcome

In this quest, you'll master CSS selectors (element, class, ID, attribute, pseudo-classes) and understand specificity—the algorithm that determines which rule wins when multiple styles target the same element.

## Concept in 30 seconds

Selectors determine **which** elements get styled. Specificity calculates **which rule wins** when conflicts occur: inline styles (highest), IDs, classes/attributes/pseudo-classes, then elements (lowest). More specific selectors override less specific ones.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/css-selectors-specificity/terms.json) and linked to the Codex:

- **selector** - Pattern determining which elements receive styles
- **specificity** - Weight determining which CSS rule wins
- **id selector** - High-specificity selector targeting by ID
- **class selector** - Medium-specificity selector targeting by class
- **pseudo-class** - Selector for elements in specific states

## Walkthrough

1. **Use element selectors**: `p`, `h1`, `div` - lowest specificity
2. **Apply class selectors**: `.button`, `.highlight` - medium specificity
3. **Target with IDs**: `#header` - high specificity (use sparingly)
4. **Combine selectors**: `.nav a` - descendant combinator
5. **Use pseudo-classes**: `:hover`, `:focus`, `:first-child`
6. **Calculate specificity**: Count IDs-Classes-Elements (1-0-0 beats 0-10-5)

## Example implementation

```css
/* Element selector (0-0-1) */
p {
  color: black;
}

/* Class selector (0-1-0) */
.highlight {
  color: blue;  /* Wins over element selector */
}

/* ID selector (1-0-0) */
#special {
  color: red;  /* Wins over class */
}

/* Combined selectors (0-2-1) */
.nav .menu-item {
  padding: 10px;
}

/* Pseudo-class (0-2-0) */
.button:hover {
  background-color: #3498db;
}

/* Attribute selector (0-1-1) */
input[type="text"] {
  border: 1px solid #ccc;
}

/* Specificity battle */
div.container p.text { color: green; }  /* 0-2-2 */
.container p { color: blue; }           /* 0-1-1 - loses */
#main p { color: purple; }              /* 1-0-1 - WINS */
```

**Selector types by specificity (low to high):**
1. Element: `div`, `p`, `h1`
2. Class: `.button`, `.active`
3. Attribute: `[type="text"]`, `[disabled]`
4. Pseudo-class: `:hover`, `:first-child`
5. ID: `#header`
6. Inline style: `style="..."`
7. `!important` (avoid!)

## Common mistakes

- **ID overuse**: IDs have high specificity, making styles hard to override
- **Using `!important`**: Nuclear option that breaks cascade, avoid except for utilities
- **Overly specific selectors**: `div#content .main article.post p.text` is unmaintainable
- **Not understanding cascade**: Same specificity? Last rule wins
- **Forgetting pseudo-class specificity**: `:hover` adds to class count

## Deep dive

Specificity is calculated as three numbers: (IDs, Classes+Attributes+Pseudo-classes, Elements+Pseudo-elements). `#nav .menu li` = (1, 1, 1). Higher left-most number wins: (0, 10, 0) loses to (1, 0, 0).

When specificity ties, **source order** decides: the last rule in the CSS file wins. This is why mobile-first media queries use `min-width`—rules for larger screens come last and override smaller breakpoints.

The `:not()` pseudo-class has zero specificity itself, but its argument counts: `.button:not(.disabled)` has specificity (0, 2, 0)—two classes.

**Best practices:**
- Prefer classes over IDs for styling
- Keep specificity low for easier overrides
- Use BEM or similar methodology to avoid specificity wars
- Reserve `!important` for utility classes like `.hidden { display: none !important; }`
