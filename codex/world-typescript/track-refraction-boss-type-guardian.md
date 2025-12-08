# Codex: Type Guardian of Refraction

> *“Any light can pass through the Prism. Only shaped light leaves it.”*

The Type Guardian watches over every boundary where JavaScript becomes TypeScript. Startups throw raw JS at the beam and call it a day; the Guardian insists on **contracts**:

- Clear domain models (`User`, `Session`, `Credentials`).
- Precise outcome types (`AuthResult` unions).
- Guards that make promises the code actually earns.

This boss is your graduation from “I use TS for autocomplete” to “I define the types that keep everyone else safe.”

---

## Mission

You receive a messy JS auth module:

- `auth.js` with functions like `login` and `getSession`.
- Status objects like `{ status: 'ok', user: {...} }` or `{ status: 'error', error: 'Invalid password' }`.
- No types, no guards, occasional `null` or `undefined` surprises.

Your task:

1. **Design a proper type model** for auth:
   - `Credentials`, `User`, `Session`.
2. **Define a discriminated union** for auth results:
   - e.g. `AuthResult = AuthSuccess | AuthFailure`.
3. **Implement type guards** to make using the result safe:
   - e.g. `isAuthSuccess(result): result is AuthSuccess`.
4. **Expose a clean API**:
   - e.g. `authenticate(credentials: Credentials): Promise<AuthResult>`.

No `any`, no blind `as`, no “it compiles if I turn off strict”. This module should feel like something you’d ship in a production TS codebase.

---

## Domain Hints

You don’t have to match these names exactly, but your design should be similar in spirit:

```ts
export type Credentials = {
  email: string;
  password: string;
};

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
}

export interface Session {
  token: string;
  user: User;
  issuedAt: string;  // ISO string
  expiresAt: string; // ISO string
}
```

For results:

```ts
export type AuthSuccess = {
  kind: 'success';
  session: Session;
};

export type AuthErrorKind =
  | 'invalid_credentials'
  | 'locked_out'
  | 'network_error';

export type AuthFailure = {
  kind: 'failure';
  reason: AuthErrorKind;
  message: string;
};

export type AuthResult = AuthSuccess | AuthFailure;
```

You may add fields (like `retryAfterSeconds`), but keep the shape coherent.

---

## API & Guards

At minimum, expose:

```ts
export async function authenticate(
  credentials: Credentials
): Promise<AuthResult> {
  // can call a fake backend or stubbed implementation in the boss scenario
}

export function isAuthSuccess(result: AuthResult): result is AuthSuccess;

export function isAuthFailure(result: AuthResult): result is AuthFailure;
```

Usage should feel like:

```ts
const result = await authenticate(creds);

if (isAuthSuccess(result)) {
  console.log(result.session.user.name);
} else {
  console.error(result.reason, result.message);
}
```

No casts required in the guarded branches.

---

## What the Guardian Cares About

**1. Type Modeling**

* Are `User`, `Session`, `Credentials` well-modeled?
* Are literal unions used where appropriate (`role`, `reason`)?
* Are nullable / optional fields explicit?

**2. Discriminated Unions & Narrowing**

* Does `AuthResult` use a shared discriminant (`kind`)?
* Do you rely on that discriminant to narrow in control flow?
* Is adding a new variant (e.g. `'mfa_required'`) straightforward?

**3. Guards & Runtime Safety**

* Do guards check enough runtime structure to be meaningful?
* After `isAuthSuccess(result)`, is the type truly safe to use?
* Are unknown or external inputs validated before being trusted?

**4. Tests**

* There should be tests covering:

  * A successful auth path.
  * At least one failure kind.
  * Guards behaving correctly (true positives and false negatives).

---

## Common Pitfalls

* Using `any` or `unknown` everywhere and casting back and forth.
* “Guards” that always return true or barely check any shape.
* A union without a shared discriminant, forcing callers to poke at multiple fields.
* No tests—just hoping the compiler is enough.

---

## Hints from the Guardian

* Start from the **public API**: what do you want consumers to see? Model that first.
* Think in **flows**: credentials → result → guard → safe usage.
* Use your **earlier Refraction quests**:

  * Q2 patterns for shared base types.
  * Q3 patterns for discriminated unions.
  * Q4 patterns for type guards.

If your final `auth.ts` is something you’d proudly review into a production codebase, you’ve passed the Guardian’s trial.
