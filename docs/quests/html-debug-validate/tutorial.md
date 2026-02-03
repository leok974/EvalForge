# Debug & Validate: Fix Broken Markup Fast

## Outcome

In this quest, you'll learn to identify and fix common HTML errors using browser DevTools, validators, and debugging strategies—understanding how to read error messages and systematically fix markup issues.

## Concept in 30 seconds

HTML errors range from minor (unclosed tags, typos) to critical (invalid nesting, missing required attributes). Browser DevTools show the parsed DOM, validators check syntax, and the console reveals warnings. Learn to read these tools to debug efficiently.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/html-debug-validate/terms.json) and linked to the Codex:

- **nesting error** - Incorrect element hierarchy or improperly closed tags
- **validator** - Tool checking HTML for syntax and structural errors
- **closing tag** - Tag marking the end of an element
- **DOM** - Document Object Model tree structure
- **devtools** - Browser developer tools for inspection

## Walkthrough

1. **Use browser DevTools**: Right-click → Inspect to view parsed HTML
2. **Check console for errors**: Red error messages indicate problems
3. **Run HTML validator**: Use W3C validator or built-in IDE validation
4. **Fix nesting issues**: Ensure tags close in correct order
5. **Validate attributes**: Check for typos in attribute names
6. **Test in multiple browsers**: Cross-browser compatibility check

## Example implementation

```html
<!-- BROKEN HTML (multiple issues) -->
<div class="container>
  <p>Welcome to <strong>our site</p></strong>
  <ul>
    <li>Item 1
    <li>Item 2</li>
  </ul>
  <img src="photo.jpg">
</div>

<!-- FIXED HTML -->
<div class="container">
  <p>Welcome to <strong>our site</strong></p>
  <ul>
    <li>Item 1</li>
    <li>Item 2</li>
  </ul>
  <img src="photo.jpg" alt="Site photo">
</div>
```

**Common error categories:**

1. **Unclosed tags**: `<div><p>text</div>` - missing `</p>`
2. **Mismatched nesting**: `<div><span></div></span>` - wrong order
3. **Missing required attributes**: `<img src="x.jpg">` - no `alt`
4. **Invalid attribute values**: `<input type="textt">` - typo in "text"
5. **Duplicate IDs**: Multiple elements with same `id`
6. **Missing quotes**: `<div class=container>` - should be `class="container"`

## Common mistakes

- **Ignoring validator warnings**: "It works in my browser" ≠ valid HTML
- **Not checking DevTools**: Errors hidden in console messages
- **Copy-paste errors**: Formatted quotes from Word become invalid characters
- **Self-closing non-void elements**: `<div />` is invalid; use `<div></div>`
- **Missing DOCTYPE**: Triggers quirks mode with unpredictable rendering
- **Incorrect character encoding**: Special characters display as � or gibberish

## Deep dive

Browser DevTools' Elements tab shows the **parsed DOM**, not your source HTML. If you wrote `<div><p></div></p>`, DevTools shows how the browser "fixed" it (probably `<div><p></p></div>` or separate siblings). This auto-correction masks errors that might behave differently across browsers.

The W3C HTML Validator (validator.w3.org) is the authoritative way to check markup. It catches subtle issues like deprecated attributes, incorrect ARIA usage, and accessibility problems. Many validators also check for common SEO issues like missing meta descriptions.

HTML error recovery varies by browser. While modern browsers handle broken HTML gracefully, edge cases produce inconsistent results. A `<table>` with improper nesting might render fine in Chrome but break in Safari. Valid HTML eliminates this uncertainty.

**Debugging strategy**:
1. Validate HTML through W3C validator
2. Open DevTools Elements panel to see parsed structure
3. Check Console for JavaScript errors (often caused by invalid HTML)
4. Use "Inspect" on problem areas to see actual DOM
5. Comment out sections to isolate the error
6. Fix one error at a time and re-validate

The DOM tree in DevTools is interactive—hover over elements to highlight them on the page, edit HTML live to test fixes, and use the "Search" function to find elements by selector or text content.
