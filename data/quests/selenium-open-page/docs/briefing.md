# Eyes on the Target

Your first mission: prove that a page exists. Before you can automate anything, you need to confirm the browser loaded the right URL.

Navigate to the Mock CMS login page and verify its `<title>` tag matches `"CMS Login"`. Print `TITLE_MATCH: <title>` to signal success to the test harness.

**Key pattern:**
```python
driver.get(app_url)
title = driver.title
assert title == "CMS Login"
print(f"TITLE_MATCH: {title}")
```

The App Preview panel shows the page for reference — your Python script drives a separate headless Chrome instance.
