## Hint 1
Import `StaleElementReferenceException` from `selenium.common.exceptions` to catch it!

## Hint 2
Do not use an explicit wait to re-query the element here, just call `driver.find_element` again to cleanly pull the newly rendered DOM node.

## Hint 3
You must click the refresh button before your old element becomes "stale"!
