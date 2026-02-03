---
id: web/html/debug-validate
title: Debugging and Validating HTML
category: html
tags: [html, debugging, validation, tools]
---

# Debugging and Validating HTML

Tools and techniques to ensure HTML is correct and error-free.

## Browser DevTools

### Inspect Element

**Chrome/Edge/Firefox:**
- Right-click element → "Inspect"
- See HTML structure and applied styles
- Edit live to test changes

### Console Errors

Check for HTML issues:
```
Open DevTools → Console tab
```

Common errors:
- Unclosed tags
- Invalid nesting
- Missing required attributes

## HTML Validation

### W3C Validator

**Online:** [validator.w3.org](https://validator.w3.org)

**Common Errors:**
- Missing DOCTYPE
- Unclosed tags
- Invalid attribute values
- Improper nesting
- Missing required attributes (`alt`, `title`)

### Browser Extensions

- **HTML Validator** (Chrome)
- **Web Developer** (Firefox)

## Common HTML Mistakes

### Unclosed Tags

```html
<!-- Bad -->
<div>
  <p>Text
</div>

<!-- Good -->
<div>
  <p>Text</p>
</div>
```

### Improper Nesting

```html
<!-- Bad -->
<p><div>Content</div></p>

<!-- Good -->
<div><p>Content</p></div>
```

### Missing Required Attributes

```html
<!-- Bad -->
<img src="photo.jpg">
<label>Email</label>

<!-- Good -->
<img src="photo.jpg" alt="Description">
<label for="email">Email</label>
```

### Block Inside Inline

```html
<!-- Bad -->
<span><div>Content</div></span>

<!-- Good -->
<div><span>Content</span></div>
```

## Accessibility Validation

### Tools

- **axe DevTools** (Browser extension)
- **WAVE** (Web Accessibility Evaluation Tool)
- **Lighthouse** (Chrome DevTools)

### Common Issues

- Missing alt text
- Poor heading hierarchy
- Low contrast
- Missing form labels
- No ARIA labels on custom controls

## Debugging Strategies

### 1. Validate Early and Often

Run HTML through validator regularly

### 2. Check Browser Console

Look for errors and warnings

### 3. Test in Multiple Browsers

- Chrome/Edge
- Firefox
- Safari
- Mobile browsers

### 4. Use DevTools

- Inspect element structure
- Check computed styles
- Test different screen sizes

### 5. Validate Accessibility

Run accessibility audits regularly

## Automated Testing

### Lighthouse

```bash
# Run from Chrome DevTools
DevTools → Lighthouse → Generate Report
```

Checks:
- Performance
- Accessibility
- Best Practices
- SEO

### HTML Hint (CLI)

```bash
npm install -g htmlhint
htmlhint index.html
```

## Best Practices

- Validate HTML before deploying
- Use semantic HTML to avoid errors
- Close all tags properly
- Include required attributes
- Test with real content
- Check accessibility compliance
- Use linters in your development workflow
- Keep HTML clean and well-formatted

## Quick Checklist

✅ DOCTYPE declared  
✅ Proper nesting  
✅ All tags closed  
✅ Required attributes present (`alt`, `for`, `lang`)  
✅ Semantic elements used where appropriate  
✅ No deprecated elements  
✅ Accessibility requirements met  
✅ Validates without errors
