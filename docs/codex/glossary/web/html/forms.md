---
id: glossary/web/html/forms
title: Forms
world: web
level: beginner
tags: [html, forms, input]
related:
  - codex:glossary/web/html/accessibility-basics
  - codex:glossary/web/html/attributes
---

# Forms

## Definition
Forms collect user input using elements like `<input>`, `<select>`, and `<textarea>`, usually with `<label>` for accessible naming.

## Usage
- Use labels tied with `for` + `id`.
- Set `name` attributes so values submit properly.
- Validate client-side + server-side.

## Example
```html
<form>
  <label for="email">Email</label>
  <input id="email" name="email" type="email" required />
</form>
```

## Pitfalls

* Placeholder text is not a label.
* Missing `name` means submitted value may be empty.

## Related

* Accessibility Basics: accessible forms use labels.
* Attributes: form elements use many attributes.