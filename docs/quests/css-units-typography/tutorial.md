# Units & Typography: Readable, Scalable Text

## Outcome

In this quest, you'll learn CSS units (px, rem, em, %, vw/vh) and typography properties to create text that's readable, accessible, and responsive across devices—understanding when to use each unit type.

## Concept in 30 seconds

Use **rem** (root em) for font sizes and spacing—it scales with user preferences. **em** is relative to parent font size. **%** and **vw/vh** adapt to container or viewport. Set base `font-size` on `:root`, use unitless `line-height`, and choose appropriate font stacks.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/css-units-typography/terms.json) and linked to the Codex:

- **rem** - Unit relative to root element font size
- **em** - Unit relative to parent element font size
- **percent** - Relative unit based on parent dimension
- **line-height** - Vertical spacing between text lines
- **font-family** - Typeface or font stack for text rendering

## Walkthrough

1. **Set root font size**: `:root { font-size: 16px; }`
2. **Use rem for scalability**: `font-size: 1.5rem` (24px if root is 16px)
3. **Apply unitless line-height**: `line-height: 1.6` (1.6× font size)
4. **Create font stack**: `font-family: 'Helvetica Neue', Arial, sans-serif;`
5. **Use web fonts**: `@font-face` or Google Fonts
6. **Set responsive typography**: Scale with viewport units or media queries

## Example implementation

```css
/* Base setup */
:root {
  font-size: 16px;  /* Default browser size */
}

/* Typography system with rem */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
  font-size: 1rem;      /* 16px */
  line-height: 1.6;     /* Unitless, relative to font size */
  color: #333;
}

h1 {
  font-size: 2.5rem;    /* 40px */
  line-height: 1.2;     /* Tight for headings */
  margin-bottom: 1rem;
}

h2 {
  font-size: 2rem;      /* 32px */
  line-height: 1.3;
}

p {
  font-size: 1rem;      /* 16px */
  margin-bottom: 1.5rem;
  max-width: 65ch;      /* Optimal line length */
}

.small-text {
  font-size: 0.875rem;  /* 14px */
}

/* Em units (relative to parent) */
.nested {
  font-size: 1.2em;     /* 1.2× parent's font size */
}

/* Responsive typography */
.hero-title {
  font-size: clamp(2rem, 5vw, 4rem);  /* Fluid between 32px-64px */
}

/* Web font loading */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
}
```

**Unit comparison:**
- `px` - Absolute, doesn't scale with user settings
- `rem` - Relative to root, scales globally
- `em` - Relative to parent, compounds in nesting
- `%` - Relative to parent's same property  
- `vw/vh` - 1% of viewport width/height
- `ch` - Width of "0" character, good for line lengths

## Common mistakes

- **Using px everywhere**: Doesn't respect user font size settings
- **Em compounding**: Nested ems multiply, hard to predict
- **Fixed line-height**: `line-height: 24px` doesn't scale with font changes
- **Missing font fallbacks**: Single font without backup breaks layout
- **Too-long lines**: Max line length should be 65-75 characters for readability

## Deep dive

The `rem` unit revolutionized responsive typography. If a user increases browser font size to 20px, `1rem` becomes 20px everywhere, maintaining proportions. This respects accessibility preferences, unlike `px` which ignores user settings.

Unitless `line-height` (e.g., `1.6`) is multiplicative: if `font-size` is 16px, line-height becomes 25.6px. If you use `line-height: 24px`, changing font size doesn't adjust line spacing, breaking rhythm. Unitless is almost always correct.

The `clamp()` function creates fluid typography: `clamp(min, preferred, max)`. For example, `font-size: clamp(1rem, 2vw, 2rem)` starts at 16px, grows with viewport, caps at 32px. This eliminates breakpoint-based font sizing.

Font stacks provide fallbacks: `font-family: 'Preferred', Fallback1, Fallback2, generic-family`. The browser uses the first available font. System font stacks like `-apple-system, BlinkMacSystemFont, 'Segoe UI'...` give native OS appearance and load instantly.

The `ch` unit equals the width of the "0" character in the current font. `max-width: 65ch` limits line length to about 65 characters, improving readability without hardcoding pixel values.

## Check yourself

Before moving on, verify you can:
- Explain the core concepts covered in this quest
- Identify common mistakes and how to avoid them
- Apply the techniques in your own projects
- Debug issues when things don't work as expected

