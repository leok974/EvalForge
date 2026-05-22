# Hints

## Hint 1
Use `page.getByRole('heading', { name: 'CMS Login' })` to locate the `<h2>` heading on the login page.

## Hint 2
The username field has `data-testid="login-username"`. Use `page.getByTestId('login-username')` to locate it.

## Hint 3
For each located element, call `await expect(element).toBeVisible()` to assert it is on the page.
