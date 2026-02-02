## Outcome
By the end of this quest you will:
- Write a small **function** that returns a value
- Print a result using **console.log**
- Understand the difference between **returning** a string and **logging** a string

## Concept in 30 seconds
JavaScript runs your code top-to-bottom. A **function** is a reusable block of code that can take inputs (**parameters**) and produce an output (**return value**).  
`console.log(...)` prints to the terminal so you can see what your program did.

**Rule of thumb:**  
- Use `return` to produce a value for *other code* to use  
- Use `console.log` to show something to the *human* running the program

## Key terms
- **console.log** — prints values to the terminal
- **string** — text like `"hello"`
- **function** — reusable code you can call by name
- **parameter** — input variable a function receives
- **return value** — the output a function gives back

## Walkthrough
1) Open `main.js`.
2) Find the `greet(name)` function.
3) Make `greet(name)` **return** a string that says: `Hello, <name>!`
4) At the bottom, we call your function and log the result.
5) Click **Run** to see the output.
6) When your output matches exactly, click **Submit**.

## Example implementation
```js
function greet(name) {
  return `Hello, ${name}!`;
}

const message = greet("Ada");
console.log(message);
```

## Common mistakes

* **Logging instead of returning**

  * Wrong: `console.log(...)` inside `greet` but no `return`
  * Fix: `return "..."` from `greet`
* **Missing quotes**

  * Wrong: `Hello, Ada!` (not in quotes)
  * Fix: `"Hello, Ada!"`
* **Using `print` (Python habit)**

  * JavaScript uses `console.log`, not `print`

## Check yourself

1. What’s the difference between `return` and `console.log`?
2. If `greet("Ada")` returns a string, where does that string go?
3. Why might you want to reuse a function instead of duplicating code?
