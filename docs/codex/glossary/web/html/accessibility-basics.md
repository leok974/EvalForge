---
id: glossary/web/html/accessibility-basics
title: Accessibility Basics
world: web
level: beginner
tags: [accessibility, a11y, best-practices]
related:
  - codex:glossary/web/html/semantic-elements
  - codex:glossary/web/html/attributes
  - codex:glossary/web/css/typography
---

# Accessibility Basics

## Definition
Accessibility (a11y) ensures interfaces are usable with screen readers, keyboard navigation, and assistive tech. Good a11y starts with semantic HTML and proper focus states.

## Usage
- Prefer semantic elements over div soup.
- Ensure keyboard focus visibility.
- Provide alt text and label inputs.

## Example
```html
<button type="button">Run Quest</button>
```

## Pitfalls

* Clickable `<div>` without keyboard support is a common a11y failure.
* Low contrast text is hard to read.

## Related

* Semantic Elements: semantic HTML improves accessibility.
* Attributes: ARIA attributes help accessibility.
* Typography: readable text improves accessibility.