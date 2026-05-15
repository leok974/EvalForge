# The Hunt for ID

You can load a page — now find what's on it. Before you can interact with a form, you need to locate its fields precisely.

Find the username and password `<input>` elements on the login page using `data-testid` CSS selectors. Print `STATUS_VALUE: found` once both elements are located.

**Key pattern:**
```python
driver.get(app_url)
username = driver.find_element(By.CSS_SELECTOR, "[data-testid='username']")
password = driver.find_element(By.CSS_SELECTOR, "[data-testid='password']")
print("STATUS_VALUE: found")
```

Use `data-testid` attributes — they are stable identifiers designed for automation, unlike class names or XPaths that break on style changes.
