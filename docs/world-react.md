# world-react — UI Foundations (Student Guide)

Welcome to the React world in [oaicite:0]{index=0}.

React is less about “writing code” and more about building a **correct mental model**:
- UI is a function of **state + props**
- state updates schedule **re-renders**
- effects synchronize React with the outside world (fetch/timers)

This guide is here so you don’t lose time on the common traps.

---

## How React quests work (EvalForge style)

### What you edit
Each quest will tell you the exact file(s) to edit in `workspace/`.
Common examples:
- `workspace/src/App.jsx`
- `workspace/src/components/...`
- `workspace/src/hooks/...`

**Rule:** Only change what the quest tells you to change.

### What the grader checks
- Rendered DOM output (text, structure, attributes)
- Interactions (click/type/submit)
- State transitions (expected UI after events)
- Async behavior (loading/error states)
- Sometimes: accessibility semantics (labels/roles)

### Your job
Make the UI:
- **deterministic**
- **accessible**
- **testable**
- **correct over time** (re-render safe)

---

## The 80/20 React mental model

### 1) Render is pure
A component is a function from **(props, state)** → UI.
If something should persist across renders, it must be:
- state (`useState`) or
- a ref (`useRef`) for mutable, non-render state

### 2) State updates are scheduled
`setState` doesn’t instantly change the value you’re holding; it schedules a re-render.
When the next value depends on the previous value, use functional updates:
```js
setCount((c) => c + 1);
setItems((xs) => [...xs, next]);
```

### 3) Effects sync React to the outside world

Use `useEffect` for:

* fetching data
* timers
* subscriptions
* manual DOM integrations

If you don’t need outside-world sync, you probably don’t need an effect.

### 4) Lists need stable keys

Keys preserve identity across renders. Bad keys = weird UI + failing tests.
Prefer stable IDs, not array indexes.

---

## What “good” looks like in EvalForge React quests

### Deterministic output

Avoid:

* `Date.now()`, random IDs, unpredictable ordering
* relying on object key iteration order
* relying on “first match” when multiple elements exist

Prefer:

* sorting before rendering where order matters
* stable IDs from fixtures / inputs
* explicit text content

### Accessible semantics (tests love this)

Prefer:

* `<button>` not `<div onClick>`
* `<label htmlFor="email">Email</label>` with `<input id="email" />`
* meaningful text on buttons (“Add item”, “Save”)

If tests can’t find elements, it’s often because labels/roles are missing.

---

## Common pitfalls (and fixes)

### “State didn’t update”

You mutated state or used the wrong update form.

Bad:

```js
items.push(x);
setItems(items);
```

Good:

```js
setItems((xs) => [...xs, x]);
```

### “My effect runs forever / infinite loop”

You update state unconditionally in an effect, or your deps change every render.

Good baseline:

```js
useEffect(() => {
  if (!id) return;
  // fetch...
}, [id]);
```

### “My list UI glitches / wrong item updates”

Keys are unstable.
Use:

```js
items.map((item) => <Row key={item.id} item={item} />);
```

### “My input won’t type”

You made it controlled but didn’t update state onChange.

```js
<input value={name} onChange={(e) => setName(e.target.value)} />
```

### “Tests fail but the UI looks fine”

Usually one of:

* wrong element type/role
* wrong text content (spacing/case)
* multiple matches (two buttons with same text)
* missing `key` or wrong deps in an effect
* async state not represented (no loading/error branch)

---

## Debugging checklist (do this before you guess)

### 1) Confirm the DOM matches expectations

* correct tag types?
* correct visible text?
* correct attributes?
* correct nesting?

### 2) Confirm state transitions

* click/typing updates state?
* are you using functional updates when needed?
* are you mutating arrays/objects?

### 3) Confirm list identity

* keys stable?
* no index keys unless list never changes order?

### 4) Confirm effects

* dependency array correct?
* cleanup needed?
* any “setState without guard” inside effect?

### 5) Confirm async behavior

* loading state exists?
* error state exists?
* stale responses handled (or ignored)?

---

## Tiny patterns (copy/paste friendly)

### Safe state updates

```js
setCount((c) => c + 1);
setItems((xs) => xs.filter((x) => x.id !== id));
setItems((xs) => [...xs, newItem]);
```

### Controlled input

```js
const [value, setValue] = useState("");
return <input value={value} onChange={(e) => setValue(e.target.value)} />;
```

### Form submit

```js
function onSubmit(e) {
  e.preventDefault();
  // validate then update
}
return <form onSubmit={onSubmit}>...</form>;
```

### Fetch effect (simple + stable)

```js
useEffect(() => {
  let alive = true;

  async function run() {
    setStatus("loading");
    try {
      const res = await fetch(url);
      const data = await res.json();
      if (!alive) return;
      setData(data);
      setStatus("ok");
    } catch {
      if (!alive) return;
      setStatus("error");
    }
  }

  run();
  return () => { alive = false; };
}, [url]);
```

### Conditional UI (recommended)

```js
if (status === "loading") return <p>Loading...</p>;
if (status === "error") return <p>Error</p>;
if (!data?.length) return <p>No results</p>;
return <List data={data} />;
```

---

## Where the Codex fits

If you’re stuck on a concept (effects, keys, controlled inputs), open:

`docs/codex/world-react/README.md`

It’s the “map + debugger” for the whole React world.

---

## Next: what to depth-pack after React

The next worlds that benefit most from this same treatment:

1. **world-node** (env, HTTP, async, tests, “why server won’t start”)
2. **world-git** (recovery + mental model prevents panic)
3. **world-infra** (Docker/networking/health checks “connection refused” playbook)
