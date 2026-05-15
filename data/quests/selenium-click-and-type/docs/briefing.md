# Data Entry Specialist

Finding elements is half the battle. Now put them to work: fill in credentials and submit the login form.

Type `admin` into the username field, `secret123` into the password field, then click the login button. A successful login redirects to the dashboard — print `LOGIN_SUCCESS` when the URL changes.

**Key pattern:**
```python
driver.find_element(By.CSS_SELECTOR, "[data-testid='username']").send_keys("admin")
driver.find_element(By.CSS_SELECTOR, "[data-testid='password']").send_keys("secret123")
driver.find_element(By.CSS_SELECTOR, "[data-testid='login-btn']").click()
print("LOGIN_SUCCESS")
```

Always clear a field before typing if it might have pre-filled content. Use `element.clear()` before `send_keys()`.
