# Accessibility Basics: Build for Everyone

## Outcome

In this quest, you'll learn essential accessibility practices to make your HTML work for keyboard users, screen readers, and people with disabilities—understanding ARIA, labels, focus management, and semantic structure.

## Concept in 30 seconds

Accessible HTML works for everyone, regardless of ability or device. Use semantic elements, provide text alternatives (`alt`, labels, ARIA labels), ensure keyboard navigation works, and maintain sufficient color contrast. Screen readers rely on proper HTML structure to navigate your content.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/html-accessibility-basics/terms.json) and linked to the Codex:

- **alt text** - Alternative text description for images
- **label association** - Explicit connection between label and form control
- **keyboard focus** - Ability to navigate using keyboard only
- **landmarks** - Semantic regions for screen reader navigation
- **ARIA** - Accessible Rich Internet Applications attributes

## Walkthrough

1. **Use semantic HTML**: Prefer `<button>` over `<div onclick>`
2. **Add alt text to images**: Describe content and function, not appearance
3. **Associate labels with inputs**: Use `for`/`id` or wrap inputs in labels
4. **Test keyboard navigation**: Tab through page, ensure all interactive elements reachable
5. **Add ARIA when HTML isn't enough**: `aria-label`, `aria-describedby`, `role`
6. **Ensure focus visibility**: Don't remove focus outlines without replacing

## Example implementation

```html
<!-- Image with descriptive alt text -->
<img 
  src="submit-button.png" 
  alt="Submit form" 
  role="button"
  tabindex="0"
>

<!-- Form with proper labels -->
<form>
  <label for="search">Search:</label>
  <input 
    type="search" 
    id="search" 
    aria-describedby="search-help"
  >
  <span id="search-help">Enter keywords to find articles</span>
  
  <button type="submit">Search</button>
</form>

<!-- Navigation with ARIA landmark -->
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<!-- Skip link for keyboard users -->
<a href="#main-content" class="skip-link">
  Skip to main content
</a>

<main id="main-content">
  <!-- Page content -->
</main>

<!-- Button vs div clickable -->
<button onclick="doAction()">Accessible Button</button>
<!-- DON'T: <div onclick="doAction()">Not a real button</div> -->
```

## Common mistakes

- **Removing focus outlines**: `outline: none` without replacement makes keyboard navigation impossible
- **Using div/span as buttons**: Missing keyboard and screen reader semantics
- **Empty alt on meaningful images**: Every informative image needs descriptive alt text
- **Not testing with keyboard**: Many accessibility issues only appear when tabbing through
- **Relying only on color**: "Click the red button" fails for colorblind users
- **Auto-playing media**: Videos that autoplay with sound violate WCAG guidelines

## Deep dive

ARIA (Accessible Rich Internet Applications) fills gaps when HTML doesn't provide needed semantics. However, the first rule of ARIA is: "Don't use ARIA if you can use native HTML instead." A native `<button>` is better than `<div role="button">` because it provides keyboard support, focus management, and clearbrowser semantics for free.

The `aria-label` attribute provides a label read by screen readers but invisible on screen. Use it when visual context is obvious but screen readers need explicit text: `<button aria-label="Close dialog">X</button>`. The `aria-describedby` attribute links an element to descriptive text elsewhere in the DOM, useful for form help text or error messages.

Keyboard accessibility requires that every interactive element is reachable via Tab/Shift+Tab and activatable via Enter or Space. Test by unplugging your mouse and navigating your entire site. If you get stuck, keyboard users will too. Custom widgets like dropdowns, modals, and carousels need  careful focus management—JavaScript must move focus appropriately when content changes.
