# The Messy Inbox

We have a data cleansing task. One of our vendor accounts has been emailing employees, but their domain was entered inconsistently into our system by the HR team. 

Some records might end in `@example.com`, others in `@Example.com` or even `@EXAMPLE.COM`.

Your mission is to write a query that finds all employees whose email contains `@example.com`, completely ignoring case. 

We need to know exactly who is registered with this external domain.
