# Responsive Design: Adapt to Any Screen

## Outcome

In this quest, you'll build responsive layouts using media queries, fluid units, and mobile-first design principles—ensuring your content looks great on phones, tablets, and desktops without separate mobile sites.

## Concept in 30 seconds

Responsive design adapts layouts to screen size using **media queries** (conditional CSS), **fluid units** (%, vw, rem), and **flexible layouts** (Flexbox/Grid). Write mobile-first CSS (small screens by default), then add `@media (min-width: ...)` for larger screens.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/css-responsive-media/terms.json) and linked to the Codex:

- **media query** - CSS rule applying styles based on device characteristics
- **breakpoint** - Screen width where layout changes
- **fluid layout** - Layout using relative units that adapt
- **viewport** - Visible area of web page in browser
- **responsive typography** - Text sizing that adapts to screen size

## Walkthrough

1. **Add viewport meta tag**: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
2. **Design mobile-first**: Base styles for small screens
3. **Add breakpoints**: `@media (min-width: 768px)` for tablets
4. **Use fluid units**: `width: 90%` instead of fixed pixels
5. **Test on devices**: Use DevTools device emulation
6. **Optimize images**: Use `srcset` for responsive images

## Example implementation

```css
/* Mobile-first base styles */
.container {
  width: 100%;
  padding: 1rem;
}

.grid {
  display: grid;
  grid-template-columns: 1fr;  /* Single column on mobile */
  gap: 1rem;
}

.nav {
  display: flex;
  flex-direction: column;  /* Stacked on mobile */
}

/* Tablet breakpoint */
@media (min-width: 768px) {
  .container {
    width: 90%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }
  
  .grid {
    grid-template-columns: repeat(2, 1fr);  /* 2 columns */
  }
  
  .nav {
    flex-direction: row;  /* Horizontal */
  }
}

/* Desktop breakpoint */
@media (min-width: 1200px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);  /* 3 columns */
  }
  
  .sidebar-layout {
    display: grid;
    grid-template-columns: 250px 1fr;
  }
}

/* Responsive typography */
:root {
  font-size: 16px;
}

@media (min-width: 768px) {
  :root {
    font-size: 18px;  /* Larger base on bigger screens */
  }
}

/* Fluid typography with clamp */
h1 {
  font-size: clamp(1.5rem, 4vw, 3rem);  /* Scales smoothly 24px-48px */
}

/* Container queries (modern) */
@container (min-width: 700px) {
  .card {
    display: flex;
  }
}

/* Print styles */
@media print {
  .no-print {
    display: none;
  }
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  body {
    background: #1a1a1a;
    color: #f0f0f0;
  }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

**Common breakpoints:**
- 640px - Large phones
- 768px - Tablets
- 1024px - Small desktops
- 1280px - Large desktops

## Common mistakes

- **Desktop-first approach**: Harder to simplify complex layouts for mobile
- **Too many breakpoints**: Creates maintenance burden, stick to 3-4 max
- **Fixed pixel widths**: Using `600px` instead of fluid `90%` or `min-width`
- **Not testing on devices**: Emulation isn't perfect, test real hardware
- **Forgetting viewport meta tag**: Site zooms out too far on mobile
- **Ignoring touch targets**: Buttons need 44×44px minimum for fingers

## Deep dive

Mobile-first CSS is easier than desktop-first because it's simpler to **add complexity** (multi-column layouts) than **remove it** (collapsing complex grids). Start with a linear, single-column mobile design, then progressively enhance with media queries.

The `min-width` media query means "at least this wide," so `@media (min-width: 768px)` applies to tablets and desktops. Since rules cascade, mobile styles apply first, then tablet rules override selectively. This keeps CSS lean—you only write the differences.

Breakpoints shouldn't target specific devices (iPhone 12, iPad Pro, etc.)—you'll never keep up with new models. Instead, choose breakpoints where **your design breaks**. Load your site, slowly resize the browser, and add breakpoints when the layout looks awkward.

The `clamp()` function creates fluid typography without media queries: `clamp(min, preferred, max)`. For example, `font-size: clamp(1rem, 2vw + 0.5rem, 2rem)` scales smoothly between 16px and 32px based on viewport width plus a fixed offset.

Preference media queries respect user settings: `prefers-color-scheme` for dark mode, `prefers-reduced-motion` for users who disabled animations (often for accessibility or motion sensitivity). Always honor these—they're explicit user preferences.

## Check yourself

Before moving on, verify you can:
- Explain the core concepts covered in this quest
- Identify common mistakes and how to avoid them
- Apply the techniques in your own projects
- Debug issues when things don't work as expected

