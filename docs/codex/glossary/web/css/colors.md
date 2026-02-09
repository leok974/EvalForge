---
id: glossary/web/css/colors
title: Colors
world: web
level: beginner
tags: [css, styling, design]
related:
  - codex:glossary/web/css/typography
  - codex:glossary/web/css/backgrounds
---

# Colors

## Definition
Colors in CSS can be defined via hex, rgb(a), hsl(a), and named colors. In UI, color must consider contrast and states (hover, focus, disabled).

## Usage
- Use CSS variables for consistent theming.
- Ensure readable contrast.
- Define state colors intentionally.

## Example
```css
:root { --text: #e6e8ee; --bg: #0b1020; }
body { color: var(--text); background: var(--bg); }
```

## Pitfalls

* Low contrast text is hard to read, especially on dark themes.
* Hardcoding colors everywhere makes theming painful.

## Related

* Typography: colors apply to text.
* Backgrounds: backgrounds use colors.