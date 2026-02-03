# Links & Images: Connect and Communicate

## Outcome

In this quest, you'll master the `<a>` anchor tag for creating links and the `<img>` tag for embedding images, understanding relative vs absolute paths, and ensuring accessibility with proper alt text.

## Concept in 30 seconds

Links (`<a href="...">`) connect pages together, while images (`<img src="..." alt="...">`) add visual content. Use relative URLs for same-site links and always provide descriptive `alt` text for screen readers and SEO.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/html-links-images/terms.json) and linked to the Codex:

- **anchor** - The `<a>` element used to create hyperlinks
- **href** - Attribute specifying link destination URL
- **relative URL** - Path relative to current page location
- **absolute URL** - Complete URL including protocol and domain
- **alt text** - Required descriptive text for images

## Walkthrough

1. **Create internal links**: `<a href="about.html">About</a>` for same-site navigation
2. **Add external links**: `<a href="https://example.com">Example</a>` with full URL
3. **Open in new tab**: Add `target="_blank"` and `rel="noopener noreferrer"`
4. **Embed images**: `<img src="photo.jpg" alt="Description">`
5. **Write meaningful alt text**: Describe image content, not just "image of..."
6. **Use responsive images**: Add `width` and `height` attributes to prevent layout shift

## Example implementation

```html
<nav>
  <a href="/">Home</a>
  <a href="/about">About</a>
  <a href="https://github.com" target="_blank" rel="noopener noreferrer">
    GitHub
  </a>
</nav>

<article>
  <h1>Web Development Basics</h1>
  
  <figure>
    <img 
      src="/images/html-structure.png" 
      alt="Diagram showing HTML document structure with head and body elements"
      width="600" 
      height="400"
    >
    <figcaption>HTML document structure</figcaption>
  </figure>
  
  <p>Learn more in our <a href="/tutorial">tutorial section</a>.</p>
</article>
```

## Common mistakes

- **Empty alt text on meaningful images**: `alt=""` should only be used for decorative images
- **Alt text like "image of"**: Screen readers already announce it's an image
- **Missing rel on external links**: `target="_blank"` without `rel="noopener"` is a security risk
- **Broken relative paths**: `href="../page.html"` doesn't match actual file structure
- **No width/height**: Browser can't reserve space, causing layout shift when image loads

## Deep dive

The `alt` attribute serves three critical purposes: it appears when images fail to load, screen readers announce it to visually impaired users, and search engines use it for image indexing. Good alt text describes the **content and function** of the image, not its appearance. For decorative images that add no information, use `alt=""` so screen readers skip them.

The `rel="noopener noreferrer"` on `target="_blank"` links prevents the new page from accessing your page's `window.opener` object—a security measure against reverse tabnabbing attacks. Modern browsers add this automatically, but it's still good practice to include explicitly.

Relative URLs like `href="about.html"` are resolved from the current page's location, while `href="/about.html"` is resolved from the domain root. Understanding this difference prevents broken links when you move pages or deploy to subfolders.

## Check yourself

Before moving on, verify you can:
- Explain the core concepts covered in this quest
- Identify common mistakes and how to avoid them
- Apply the techniques in your own projects
- Debug issues when things don't work as expected

