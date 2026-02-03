# Metadata & SEO Basics: Be Discoverable

## Outcome

In this quest, you'll add essential metadata to your HTML `<head>` section to control how browsers, search engines, and social media platforms understand and display your pages.

## Concept in 30 seconds

The `<head>` section contains invisible metadata: `<title>` for browser tabs and search results, `<meta name="description">` for search snippets, viewport settings for mobile, and Open Graph tags for social media previews. Proper metadata improves SEO, shareability, and user experience.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/html-meta-seo/terms.json) and linked to the Codex:

- **title tag** - Page title in browser tab and search results
- **meta description** - Summary shown in search engine results
- **viewport** - Meta tag controlling mobile browser layout
- **charset** - Character encoding declaration
- **open graph** - Meta tags for social media previews

## Walkthrough

1. **Set page title**: Unique, descriptive, 50-60 characters
2. **Add meta description**: Compelling summary, 150-160 characters
3. **Configure viewport**: Enable responsive design on mobile
4. **Declare charset**: UTF-8 for international character support
5. **Add Open Graph tags**: Control how links appear on social media
6. **Include favicon**: Icon displayed in browser tab

## Example implementation

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Essential meta tags -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <!-- SEO meta tags -->
  <title>Web Development Tutorial | Learn HTML & CSS</title>
  <meta 
    name="description" 
    content="Comprehensive guide to web development fundamentals. Learn HTML structure, CSS styling, and best practices for building modern websites."
  >
  <meta name="keywords" content="HTML, CSS, web development, tutorial">
  <meta name="author" content="Your Name">
  
  <!-- Open Graph for social media -->
  <meta property="og:title" content="Web Development Tutorial">
  <meta property="og:description" content="Learn HTML & CSS fundamentals">
  <meta property="og:image" content="https://example.com/preview.jpg">
  <meta property="og:url" content="https://example.com/tutorial">
  <meta property="og:type" content="website">
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Web Development Tutorial">
  <meta name="twitter:description" content="Learn HTML & CSS fundamentals">
  <meta name="twitter:image" content="https://example.com/preview.jpg">
  
  <!-- Favicon -->
  <link rel="icon" type="image/png" href="/favicon.png">
  
  <!-- Canonical URL (prevents duplicate content issues) -->
  <link rel="canonical" href="https://example.com/tutorial">
</head>
<body>
  <!-- Page content -->
</body>
</html>
```

## Common mistakes

- **Generic titles**: "Home Page" doesn't help users or search engines
- **Missing meta description**: Search engines generate poor snippets from page content
- **Duplicate titles across pages**: Every page needs unique title and description
- **Too long/short descriptions**: Optimal is 150-160 chars; longer gets truncated
- **No viewport meta tag**: Site doesn't work properly on mobile devices
- **Forgetting Open Graph**: Links shared on social media look unprofessional

## Deep dive

The `<title>` appears in three critical places: browser tabs, search engine results, and social media shares. It should be unique per page, descriptive, and include keywords naturally. Format: "Page Name | Category | Site Name" works well, e.g., "Chocolate Chip Cookies | Recipes | Cooking Blog."

Meta descriptions don't directly affect search rankings, but they significantly impact click-through rates. Write compelling copy that summarizes the page and includes a call-to-action. Think of it as ad copy—you have 160 characters to convince someone to click.

Open Graph tags were created by Facebook but are now used by LinkedIn, Discord, Slack, and many platforms. The `og:image` should be at least 1200×630 pixels for best quality. Without these tags, platforms generate previews from whatever content they find, often showing poor or misleading snippets.

The canonical URL (`<link rel="canonical">`) tells search engines which version of a page is authoritative when the same content appears at multiple URLs (e.g., with/without www, http/https, with URL parameters). This prevents duplicate content penalties and consolidates SEO value to one URL.
