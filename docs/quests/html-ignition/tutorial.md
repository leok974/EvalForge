# HTML Ignition: Your First Page

## Outcome

In this quest, you'll build your first valid HTML5 page from scratch, understanding the essential structure every web page needs. You'll confirm it renders correctly in a browser and validates without errors.

## Concept in 30 seconds

Every HTML document follows the same foundational pattern: a DOCTYPE declaration, a `<html>` container, a `<head>` section for metadata, and a `<body>` section for visible content. This skeleton structure ensures browsers render your page correctly and search engines can index it properly.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/html-ignition/terms.json) and linked to the Codex:

- **doctype** - Declaration that defines the HTML version
- **head** - Container for metadata and page configuration  
- **body** - Container for visible page content
- **meta charset** - Character encoding declaration
- **viewport** - Meta tag controlling mobile layout

## Walkthrough

1. **Create the DOCTYPE**: Start with `<!DOCTYPE html>` to declare HTML5
2. **Add html element**: Wrap everything in `<html lang="en">`
3. **Build the head**: Include `<meta charset="UTF-8">` and viewport meta tag
4. **Add a title**: `<title>` text appears in browser tab
5. **Create the body**: Add visible content inside `<body>`
6. **Validate**: Open in browser and check for errors

## Example implementation

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My First Page</title>
</head>
<body>
  <h1>Hello, World!</h1>
  <p>This is my first valid HTML page.</p>
</body>
</html>
```

## Common mistakes

- **Missing DOCTYPE**: Browser enters quirks mode, rendering inconsistently
- **No viewport meta tag**: Page doesn't scale correctly on mobile devices  
- **Forgot charset**: Special characters display as gibberish
- **Empty title**: Browser tab shows file path instead of meaningful title

## Deep dive

The `<!DOCTYPE html>` declaration isn't technically an HTML tag—it's an instruction to the browser about which HTML version to expect. HTML5 simplified this dramatically from earlier versions that required long, complex DOCTYPE strings. The `lang="en"` attribute on the `<html>` element helps screen readers pronounce content correctly and assists search engines with language detection.

The viewport meta tag was introduced for mobile browsers. Without it, mobile browsers assume pages are designed for desktop (typically 980px wide) and shrink everything down. The `width=device-width, initial-scale=1.0` setting tells mobile browsers to match the screen width and not apply zoom.
