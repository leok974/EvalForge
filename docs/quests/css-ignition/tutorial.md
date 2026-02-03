# CSS Ignition: Your First Styles

## Outcome

In this quest, you'll link a CSS stylesheet to HTML and apply basic styles using selectors, properties, and declarations—understanding how CSS transforms plain markup into visually styled content.

## Concept in 30 seconds

CSS (Cascading Style Sheets) separates presentation from content. You link a `.css` file with `<link rel="stylesheet">`, then write rules: a **selector** targets elements, and **declarations** (property-value pairs) define their appearance.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/css-ignition/terms.json) and linked to the Codex:

- **stylesheet** - External CSS file linked to HTML
- **selector** - Pattern targeting HTML elements for styling
- **property** - CSS attribute controlling style aspect
- **declaration** - Property-value pair in a CSS rule
- **class selector** - Selector targeting elements by class

## Walkthrough

1. **Create stylesheet**: Make a `styles.css` file
2. **Link to HTML**: Add `<link rel="stylesheet" href="styles.css">` in `<head>`
3. **Write a rule**: `selector { property: value; }`
4. **Use element selectors**: `p { color: blue; }`
5. **Apply classes**: `.highlight { background: yellow; }`
6. **Verify in browser**: Refresh and see styles applied

## Example implementation

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>My Styled Page</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <h1 class="page-title">Welcome</h1>
  <p class="intro">This is a styled paragraph.</p>
  <p>This is a normal paragraph.</p>
</body>
</html>
```

```css
/* styles.css */

/* Element selector */
body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  margin: 20px;
}

/* Class selector */
.page-title {
  color: #2c3e50;
  font-size: 2em;
  border-bottom: 2px solid #3498db;
}

.intro {
  font-size: 1.2em;
  color: #555;
  background-color: #f4f4f4;
  padding: 10px;
}

/* Element selector */
p {
  margin-bottom: 15px;
}
```

## Common mistakes

- **Wrong file path**: `href="style.css"` when file is `styles.css`
- **Missing link tag**: CSS file exists but isn't linked to HTML
- **Syntax errors**: Forgetting semicolons, braces, or colons
- **Specificity confusion**: More specific selectors override general ones
- **Inline styles**: Using `style=""` attribute instead of external CSS

## Deep dive

The cascade in CSS means rules flow down from general to specific. If you style `body { color: black; }` and `p { color: blue; }`, paragraphs inherit the body's styles except where overridden. Understanding this prevents redundant declarations.

Class selectors (`.classname`) are reusable across multiple elements, while ID selectors (`#idname`) should only target one element. Classes are preferred for styling because they're flexible and maintainable.

The browser's DevTools lets you see which styles apply to each element, which are overridden, and where they come from. Right-click an element → Inspect → Styles panel shows the computed styles and the cascade order. Struck-through rules were overridden by more specific selectors.

## Check yourself

Before moving on, verify you can:
- Explain the core concepts covered in this quest
- Identify common mistakes and how to avoid them
- Apply the techniques in your own projects
- Debug issues when things don't work as expected

