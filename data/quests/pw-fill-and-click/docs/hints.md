# Hints

## Hint 1
The username field has `data-testid="login-username"` and the password field has `data-testid="login-password"`. Use `page.getByTestId(...)`.

## Hint 2
The password is `secret123` (not `admin`). Using wrong credentials will show an error and stay on `/login`.

## Hint 3
After clicking submit, use `await expect(page).toHaveURL(/dashboard/)` to assert the redirect happened.
