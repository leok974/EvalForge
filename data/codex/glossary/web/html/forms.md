---
id: web/html/forms
title: HTML Forms
category: html
tags: [html, forms, input]
---

# HTML Forms

Forms collect user input and submit data to servers.

## Basic Structure

```html
<form action="/submit" method="post">
  <label for="name">Name:</label>
  <input type="text" id="name" name="name" required>
  
  <button type="submit">Submit</button>
</form>
```

## Form Attributes

- **`action`**: URL to submit data
- **`method`**: `get` or `post`
- **`enctype`**: Encoding type (for file uploads use `multipart/form-data`)

## Input Types

```html
<input type="text">      <!-- Text field -->
<input type="email">     <!-- Email validation -->
<input type="password">  <!-- Hidden input -->
<input type="number">    <!-- Numeric input -->
<input type="checkbox">  <!-- Checkbox -->
<input type="radio">     <!-- Radio button -->
<input type="file">      <!-- File upload -->
<input type="date">      <!-- Date picker -->
```

## Form Controls

```html
<textarea rows="4">Multi-line text</textarea>

<select name="option">
  <option value="1">Option 1</option>
  <option value="2">Option 2</option>
</select>

<button type="submit">Submit</button>
<button type="reset">Reset</button>
```

## Validation Attributes

- `required`: Field must be filled
- `pattern`: Regular expression validation
- `min`, `max`: Numeric/date ranges
- `minlength`, `maxlength`: Character limits

## Best Practices

- Always associate `<label>` with inputs using `for`/`id`
- Use appropriate `type` for validation
- Provide clear error messages
- Include `name` attribute for server processing
