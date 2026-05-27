## Hint 1
You will need to use `driver.get()` to execute the navigation. The target URL is stored in the `app_url` variable.

## Hint 2
Once the page is loaded, you can access the title of the document using `driver.title`. Make sure to print it as instructed in the console output!

## Hint 3
If the title assertion is failing, verify you navigated to `app_url` (passed into
your function) rather than a hardcoded string. The mock CMS page title is exactly
`"CMS Login"`. Add `print(driver.title)` before your assertion to debug what the
browser sees.
