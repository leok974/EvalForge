---
id: glossary/web/css/inheritance
title: Inheritance
world: web
level: beginner
tags: [css, inheritance, fundamentals]
related:
  - codex:glossary/web/css/typography
  - codex:glossary/web/css/cascade
---

# Inheritance

## Definition
Some CSS properties inherit from parents (like `color` and `font-family`), while others don't (like `margin` and `padding`). Inheritance reduces repetition but can cause surprises.

## Usage
- Set base typography on `body`.
- Use inheritance for consistent text styling.
- Override locally when needed.

## Example
```css
body { color: #e6e8ee; font-family: system-ui; }
```

## Pitfalls

* Inherited colors can make nested components unreadable.
* Assuming layout properties inherit leads to confusion.

## Related

* Typography: typography properties inherit.
* Cascade: inheritance interacts with the cascade.