## Hint 1
Start by copying your successful `login` script from previous quests!

## Hint 2
You'll need `By.CSS_SELECTOR` to grab the username and password fields.

## Hint 3
Don't forget `WebDriverWait` before checking `driver.current_url`.

## Hint 4
If the title is "Admin", using `title.text.lower()` with `"admin"` inside your assert statement is a safe way to check regardless of case changes.
