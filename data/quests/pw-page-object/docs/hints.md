# Hints

## Hint 1
Your `LoginPage` class needs an `async login(username: string, password: string)` method.

## Hint 2
Inside `login()`, use `this.page.getByTestId('login-username').fill(username)` etc.

## Hint 3
After calling `await loginPage.login('admin', 'secret123')`, assert `await expect(page).toHaveURL(/dashboard/)`.
