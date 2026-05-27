## Hint 1
You cannot click an element that relies on CSS `display: none;`! Use `visibility_of_element_located`.

## Hint 2
Don't forget that `.until(EC.visibility_of_element_located(...))` requires a nested tuple `((By.CSS_SELECTOR, "..."))`. Note the double parentheses!

## Hint 3
Avoid `time.sleep()`. Using it will fail automated code audits.
