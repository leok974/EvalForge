# Tags & Attributes: Structure With Intent

## Outcome

In this quest, you'll learn to use HTML tags correctly, understanding the difference between elements and attributes, and how to structure content with proper nesting and meaningful attributes.

## Concept in 30 seconds

HTML uses **elements** (tag pairs with content between) and **attributes** (name-value pairs that add meaning). Proper nesting creates a tree structure, and semantic attributes like `id`, `class`, and `aria-label` make your content accessible and styleable.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/html-tags-attributes/terms.json) and linked to the Codex:

- **element** - Complete structure of opening tag, content, and closing tag
- **attribute** - Name-value pairs adding configuration to elements
- **nesting** - Placing elements inside others following hierarchy rules
- **id** - Unique identifier for a single element
- **class** - Grouping attribute for styling or scripting

## Walkthrough

1. **Understand element syntax**: `<tagname>content</tagname>`
2. **Add attributes**: `<tagname attribute="value">content</tagname>`
3. **Practice nesting**: Place child elements fully inside parent elements
4. **Use semantic attributes**: Add `id` for unique elements, `class` for groups
5. **Close tags properly**: Every opening tag needs a matching closing tag
6. **Validate structure**: Use browser DevTools to inspect the DOM tree

## Example implementation

```html
<article id="blog-post-1" class="featured-post">
  <header class="post-header">
    <h1>Understanding HTML Structure</h1>
    <p class="author">By <span class="author-name">Jane Doe</span></p>
  </header>
  
  <div class="post-content">
    <p>HTML elements can be <strong>nested</strong> to create hierarchy.</p>
    <ul class="key-points">
      <li>Elements have opening and closing tags</li>
      <li>Attributes provide additional information</li>
      <li>Proper nesting creates semantic structure</li>
    </ul>
  </div>
</article>
```

## Common mistakes

- **Overlapping tags**: `<p><strong>text</p></strong>` - closing tags in wrong order
- **Missing closing tags**: `<div><p>text</div>` - forgot to close `<p>`
- **Duplicate IDs**: Multiple elements with `id="header"` - IDs must be unique
- **Mismatched quotes**: `<div class="container'>` - mixing single and double quotes

## Deep dive

The DOM (Document Object Model) is built from your HTML element tree. When you write `<div><p>text</p></div>`, the browser creates a parent `div` node with a child `p` node. This parent-child relationship affects CSS inheritance, JavaScript traversal, and accessibility navigation.

Attributes come in two flavors: **global attributes** work on any element (`id`, `class`, `title`, `aria-*`), while **element-specific attributes** only make sense on certain elements (`href` on `<a>`, `src` on `<img>`). Boolean attributes like `disabled` or `checked` don't need values—their presence alone activates the behavior.
