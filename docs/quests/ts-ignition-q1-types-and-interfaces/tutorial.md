## Outcome
By the end of this quest you will:
- Define an **interface** to describe an object shape
- Use a **type alias** (including a **union type**)
- Write a function that accepts a typed object and returns a typed value

## Concept in 30 seconds
TypeScript is JavaScript with **types**. Types help you catch mistakes *before* running the program.  
Important: types do not run at runtime — TypeScript checks your code, then your program runs as JavaScript.

**Mental model:**  
Types are like labels on boxes. They don’t change the box, but they help you avoid putting the wrong thing inside.

## Key terms
- **type annotation** — attaching a type to a value (e.g., `name: string`)
- **interface** — a named object “shape”
- **type alias** — a named type, often used for unions
- **union type** — “either A or B” (e.g., `string | number`)
- **compiler** — checks types and reports errors

## Walkthrough
1) Open `main.ts`.
2) Create a type alias `Id` that can be a `string` or a `number`.
3) Create an interface `User` with:
   - `id: Id`
   - `name: string`
4) Implement `formatUser(user: User): string` that returns: `<id>: <name>`
5) Run the file and confirm the printed output.
6) Submit when it passes.

## Example implementation
```ts
type Id = string | number;

interface User {
  id: Id;
  name: string;
}

function formatUser(user: User): string {
  return `${user.id}: ${user.name}`;
}

console.log(formatUser({ id: 1, name: "Ada" }));
```

## Common mistakes

* **Using `String` instead of `string`**

  * Prefer primitives: `string`, `number`, `boolean`
* **Forgetting the union**

  * If `id` should allow both, write `string | number`
* **Assuming types run at runtime**

  * TypeScript won’t “convert” values for you. If you need runtime checks, write code like `typeof user.id === "string"`.

## Check yourself

1. Why might you use `string | number` instead of only `number`?
2. What does an interface describe?
3. Do TypeScript types exist when your program runs?
