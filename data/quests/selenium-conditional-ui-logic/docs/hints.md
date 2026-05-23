## Hint 1
Make sure you import `selenium.common.exceptions.TimeoutException` exactly as written!

## Hint 2
You only want to wait 1 or 2 seconds in your `try` block. If you wait 10 seconds, and the modal `show_modal=false` isn't there, your script slows down needlessly!

## Hint 3
If you do catch the modal, remember to click `[data-testid='modal-cancel']` or you'll be blocked.
