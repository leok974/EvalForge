## Hint 1
Did your script crash immediately? Did you accidentally type `find_element` instead of `find_elements`? Look out for that plural 's'!

## Hint 2
It is perfectly legal in Python to use `row.find_element(By.CSS_SELECTOR, "...")` to scope your search strictly within that specific ticket.

## Hint 3
Don't forget that `.text` evaluates to a string. Make sure you check if it's `in` your allowed valid list!
