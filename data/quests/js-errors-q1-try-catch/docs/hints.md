## Hint 1
Wrap code that might throw in a `try` block and handle the error in `catch`:
```js
try {
  JSON.parse("not json");
} catch (err) {
  console.error("Parse failed:", err.message);
}
```
The grader checks your source for `try` and `catch` keywords.

## Hint 2
To throw your own error:
```js
if (!input) throw new Error("Input is required");
```
The `finally` block runs whether or not an error was thrown — useful for cleanup.
