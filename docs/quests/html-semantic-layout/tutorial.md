# Semantic Layout: Landmarks That Make Sense

## Outcome

In this quest, you'll structure page layouts using HTML5 semantic elements (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`) to create accessible landmarks that help both humans and machines understand your content.

## Concept in 30 seconds

Semantic elements describe their content's purpose, not just appearance. `<header>` contains introductory content, `<nav>` holds navigation links, `<main>` wraps primary content, etc. Screen readers use these landmarks for quick navigation, and search engines use them to understand page structure.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/html-semantic-layout/terms.json) and linked to the Codex:

- **semantic elements** - HTML5 tags that convey meaning about content
- **landmarks** - Major page regions identifiable by assistive technology
- **header** - Introductory content or navigation container
- **nav** - Section containing navigation links
- **main** - Primary content of the document (one per page)

## Walkthrough

1. **Add page header**: `<header>` with logo and site navigation
2. **Create nav landmark**: `<nav>` with primary navigation links
3. **Define main content**: `<main>` wrapping the page's primary purpose
4. **Use article for independent content**: Blog posts, forum posts, news articles
5. **Group related content in sections**: `<section>` for thematic grouping
6. **Add page footer**: `<footer>` with copyright, secondary nav, contact info

## Example implementation

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Semantic Page Structure</title>
</head>
<body>
  <header>
    <h1>Site Name</h1>
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
  </header>
  
  <main>
    <article>
      <header>
        <h2>Article Title</h2>
        <p>Published on <time datetime="2026-02-02">February 2, 2026</time></p>
      </header>
      
      <section>
        <h3>Introduction</h3>
        <p>Article introduction goes here...</p>
      </section>
      
      <section>
        <h3>Main Points</h3>
        <p>Key information...</p>
      </section>
    </article>
    
    <aside>
      <h3>Related Articles</h3>
      <ul>
        <li><a href="/related-1">Related Article 1</a></li>
        <li><a href="/related-2">Related Article 2</a></li>
      </ul>
    </aside>
  </main>
  
  <footer>
    <p>&copy; 2026 Site Name. All rights reserved.</p>
  </footer>
</body>
</html>
```

## Common mistakes

- **Multiple `<main>` elements**: Only one `<main>` per page (the primary content area)
- **Nesting main inside article**: `<main>` should be top-level, articles go inside it
- **Using nav for all links**: Reserve `<nav>` for major navigation groups, not every link
- **div soup**: Using `<div>` when semantic elements would be more appropriate
- **Header/footer confusion**: `<header>` isn't just for page top—articles can have headers too

## Deep dive

Screen readers provide landmark navigation via keyboard shortcuts. Users can press "H" to cycle through headers, "N" for nav regions, "M" to jump to main content, etc. Without semantic landmarks, blind users must listen to the entire page sequentially or navigate by headings alone.

The `<article>` element represents self-contained, independently distributable content. Ask: "Could this stand alone in an RSS feed or on another site?" If yes, use `<article>`. A blog post is an `<article>`; so is each product in a catalog or each comment in a thread.

The `<section>` element groups related content thematically. Unlike `<div>` (no semantic meaning), `<section>` indicates "this content belongs together." Sections typically have a heading. If you can't describe the section's purpose with a heading, you probably want `<div>` instead.

## Check yourself

Before moving on, verify you can:
- Explain the core concepts covered in this quest
- Identify common mistakes and how to avoid them
- Apply the techniques in your own projects
- Debug issues when things don't work as expected

