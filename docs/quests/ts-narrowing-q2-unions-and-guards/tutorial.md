## Outcome
By the end of this quest you will:
- Use **typeof** to narrow `string | number`
- Use the **in** operator to narrow object shapes safely
- Use a **discriminated union** (a `kind` field) to pick the right branch
- Write a **type guard** (`value is X`) that makes TypeScript smarter

## Concept in 30 seconds
TypeScript lets a variable have more than one possible type (a **union**), like `string | number`.
To use a union safely, you narrow it at runtime:
- `typeof x === "string"` narrows `x` to string
- `"email" in obj` checks if a property exists
- A `kind` field like `"email" | "phone"` is a reliable switch (discriminated union)

**Mental model:**  
Runtime checks (if/switch) are the “evidence” that lets TypeScript safely treat a value as a specific type.

## Key terms
- **type narrowing** — turning a union into a specific type using checks
- **type guard** — a function that returns `value is SomeType`
- **discriminated union** — union with a shared `kind` field
- **typeof** — checks runtime primitive type (string/number/boolean/…)
- **in operator** — checks if a property exists on an object

## Walkthrough
1) Open `main.ts`.
2) Implement `normalizeId(id)`:
   - If `id` is a number, return it.
   - If `id` is a string, trim it and parse an integer.
   - If parsing fails, return `null`.
3) Implement `isContact(value)` as a **type guard** for `Contact`.
   - It should return `true` only for valid Contact objects.
4) Implement `formatContact(contact)` using `contact.kind`:
   - `"email"` → `email:<email>`
   - `"phone"` → `phone:<phone>`
5) Click **Run** to see demo output.
6) Click **Submit** when tests pass.

## Example implementation
```ts
export type Contact =
  | { kind: "email"; email: string }
  | { kind: "phone"; phone: string };

export function normalizeId(id: string | number): number | null {
  if (typeof id === "number") return id;

  const trimmed = id.trim();
  const n = Number.parseInt(trimmed, 10);
  return Number.isNaN(n) ? null : n;
}

export function isContact(value: unknown): value is Contact {
  if (typeof value !== "object" || value === null) return false;

  // We’ll safely probe properties using `in`
  if (!("kind" in value)) return false;

  const v = value as any;
  if (v.kind === "email") return typeof v.email === "string";
  if (v.kind === "phone") return typeof v.phone === "string";
  return false;
}

export function formatContact(contact: Contact): string {
  switch (contact.kind) {
    case "email":
      return `email:${contact.email}`;
    case "phone":
      return `phone:${contact.phone}`;
  }
}
```

## Common mistakes

* **Using `as Contact` too early**

  * That bypasses safety. Use checks (`typeof`, `in`, discriminant) first.
* **Forgetting `value === null`**

  * `typeof null === "object"`, so always check null explicitly.
* **Not narrowing the discriminant**

  * Prefer `switch (contact.kind)` over guessing fields exist.
* **Parsing without validation**

  * `parseInt("abc")` gives `NaN`. Always handle `NaN`.

## Check yourself

1. Why is a `kind` field helpful for unions?
2. What does `value is Contact` do for TypeScript?
3. Why must we check `value !== null` before using `in`?
