# Cascade & Inheritance: Predict Rule Outcomes

## Outcome

In this quest, you'll understand the CSS cascade (how conflicting rules are resolved) and inheritance (how property values flow from parents to children)—enabling you to predict which styles apply and write more efficient CSS.

## Concept in 30 seconds

The **cascade** resolves conflicts using importance, specificity, and source order. **Inheritance** passes certain properties (like `color`, `font-family`) from parents to children automatically, while others (like `border`, `margin`) don't inherit.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/css-cascade-inheritance/terms.json) and linked to the Codex:

- **cascade** - Algorithm CSS uses to resolve conflicting rules
- **inheritance** - Process where child elements inherit parent styles
- **source order** - Position in stylesheet affects which rule wins
- **computed value** - Final resolved value after cascade and inheritance
- **initial value** - Default value defined by CSS specification

## Walkthrough

1. **Understand cascade order**: Importance → Specificity → Source Order
2. **Identify inherited properties**: Typography (`color`, `font-*`, `line-height`)
3. **Use `inherit` keyword**: Force inheritance for non-inherited properties
4. **Apply `initial` keyword**: Reset to spec default value
5. **Leverage cascade**: Define base styles on parent, override on children
6. **Observe DevTools**: See which rules apply and which are overridden

## Example implementation

```css
/* Base styles on body cascade down */
body {
  color: #333;           /* Inherited by all text */
  font-family: Arial;    /* Inherited */
  line-height: 1.6;      /* Inherited */
  margin: 0;             /* NOT inherited */
}

/* Child inherits text properties */
p {
  /* Already has color: #333 from body */
  margin-bottom: 1em;    /* NOT inherited from any parent */
}

/* Explicitly inherit */
.special-link {
  color: inherit;  /* Inherits from parent, not default blue */
}

/* Force inheritance */
button {
  font-family: inherit;  /* Buttons don't inherit by default */
}

/* Reset to initial value */
.reset {
  color: initial;  /* Black (browser default) */
}

/* Cascade specificity battle */
.container p {
  color: blue;     /* 0-1-1 */
}

p.highlight {
  color: red;      /* 0-1-1 - BUT comes later, WINS */
}

/* Higher specificity always wins */
#main .container p {
  color: green;    /* 1-1-1 - WINS regardless of order */
}
```

**Properties that inherit:**
- Text: `color`, `font-*`, `line-height`, `text-align`, `text-transform`
- Lists: `list-style-*`
- Some others: `cursor`, `visibility`

**Properties that DON'T inherit:**
- Box model: `margin`, `padding`, `border`, `width`, `height`
- Positioning: `position`, `top`, `left`
- Layout: `display`, `float`
- Most others

## Common mistakes

- **Expecting box model to inherit**: `margin` and `padding` never inherit
- **Not leveraging inheritance**: Re-declaring `font-family` on every element
- **Fighting the cascade**: Using `!important` instead of understanding specificity
- **Assuming all properties inherit**: Only typography and a few others do
- **Forgetting source order**: Same specificity? Last rule wins

## Deep dive

The cascade's three layers work in order: **Importance** (`!important` user styles → `!important` author styles → normal), **Specificity** (ID > class > element), **Source Order** (last wins).

Inheritance exists for efficiency. Setting `color: black` on `body` means all text inherits that color—you don't re-declare it on every `<p>`, `<h1>`, `<li>`, etc. This creates a natural "theme" that flows through your document.

The `inherit`, `initial`, `unset`, and `revert` keywords give fine control:
- `inherit` - Use parent's value
- `initial` - Use CSS spec default
- `unset` - `inherit` if normally inheritable, `initial` otherwise  
- `revert` - Roll back to user agent stylesheet

Understanding cascade and inheritance prevents specificity battles and makes CSS predictable. When in doubt, check DevTools' Computed tab to see the final value and which rule provided it.

## Check yourself

Before moving on, verify you can:
- Explain the core concepts covered in this quest
- Identify common mistakes and how to avoid them
- Apply the techniques in your own projects
- Debug issues when things don't work as expected

