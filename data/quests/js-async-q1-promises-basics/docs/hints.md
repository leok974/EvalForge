## Hint 1
A `Promise` represents a value that will be available in the future. Create one with:
```js
const p = new Promise((resolve, reject) => {
  // call resolve(value) on success, reject(error) on failure
  resolve(42);
});
```
The grader checks your source for the `Promise` constructor or `async`/`await`.

## Hint 2
To consume a promise, chain `.then()` and `.catch()`:
```js
p.then(value => console.log(value))
 .catch(err => console.error(err));
```
Or use `async/await` inside an `async` function:
```js
async function run() {
  const value = await p;
}
```
