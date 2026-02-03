# Forms & Inputs: Collect User Data

## Outcome

In this quest, you'll build accessible HTML forms that collect user input, understanding form elements, input types, labels, validation attributes, and proper form submission handling.

## Concept in 30 seconds

Forms (`<form>`) contain controls like `<input>`, `<select>`, and `<textarea>` for user data entry. Every control needs a `<label>` for accessibility, a `name` attribute for server submission, and appropriate `type` for validation and mobile keyboard optimization.

## Key terms

The key terms for this quest are defined in [terms.json](file:///d:/EvalForge/docs/quests/html-forms-inputs/terms.json) and linked to the Codex:

- **form** - Container element for collecting user input
- **input** - Form control with various types (text, email, checkbox, etc.)
- **label** - Text associated with a form control for accessibility
- **name attribute** - Identifies field data when submitted to server
- **validation** - Client-side checking before submission

## Walkthrough

1. **Create form container**: `<form action="/submit" method="POST">`
2. **Add labeled inputs**: Wrap each input with associated `<label>`
3. **Use meaningful input types**: email, tel, date, number for mobile keyboards
4. **Add validation**: required, pattern, min/max attributes
5. **Include submit button**: `<button type="submit">` inside the form
6. **Test keyboard navigation**: Tab through all controls, press Enter to submit

## Example implementation

```html
<form action="/register" method="POST">
  <div>
    <label for="username">Username:</label>
    <input 
      type="text" 
      id="username" 
      name="username" 
      required 
      minlength="3"
      autocomplete="username"
    >
  </div>
  
  <div>
    <label for="email">Email:</label>
    <input 
      type="email" 
      id="email" 
      name="email" 
      required
      autocomplete="email"
    >
  </div>
  
  <div>
    <label for="age">Age:</label>
    <input 
      type="number" 
      id="age" 
      name="age" 
      min="13" 
      max="120"
    >
  </div>
  
  <div>
    <label for="bio">Bio:</label>
    <textarea 
      id="bio" 
      name="bio" 
      rows="4" 
      maxlength="500"
    ></textarea>
  </div>
  
  <div>
    <input type="checkbox" id="terms" name="terms" required>
    <label for="terms">I agree to the terms</label>
  </div>
  
  <button type="submit">Register</button>
</form>
```

## Common mistakes

- **Missing label association**: `<label>Username</label><input>` without `for`/`id` connection
- **Using placeholder as label**: Placeholders disappear on focus and aren't accessible
- **Generic input types**: Using `type="text"` for email/phone prevents mobile keyboard optimization
- **No validation feedback**: Required fields without visual indication or error messages
- **Button outside form**: Submit button must be inside `<form>` to work

## Deep dive

The `for` attribute on `<label>` must match the `id` of its input. This creates an explicit association so clicking the label focuses the input, and screen readers announce the label when the input receives focus. For checkboxes and radios, this clickable area is especially important for usability.

Input types like `type="email"` provide three benefits: (1) mobile browsers show optimized keyboards with @ symbol, (2) browsers provide built-in format validation, and (3) screen readers announce "email field" to set expectations. The `autocomplete` attribute helps browsers and password managers fill forms correctly.

HTML5 validation (`required`, `pattern`, `min`, `max`) happens before form submission, preventing unnecessary server requests. However, never trust client-side validation alone—always validate on the server as well, since users can bypass HTML validation via browser dev tools.

## Check yourself

Before moving on, verify you can:
- Explain the core concepts covered in this quest
- Identify common mistakes and how to avoid them
- Apply the techniques in your own projects
- Debug issues when things don't work as expected

