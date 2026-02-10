### Quest Packet: react-components

**README.md**

```md
# React Components: Composition

Edit `task.mjs` to export two components: `Card` and `CardBody`.

Requirements:
1. `CardBody` should render a `div` with `data-testid="card-body"` and text "I am the body".
2. `Card` should render a `div` with `data-testid="card"`.
3. `Card` should render `CardBody` as a child (nested inside the div).

Structure:
<div data-testid="card">
  <div data-testid="card-body">I am the body</div>
</div>

```

**Public Test**

```javascript
import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId } from "../../../_shared/react_test_helpers.mjs";
import { Card, CardBody } from "../../workspace/task.mjs";

test("Card renders CardBody", () => {
    const { root } = runComponent(Card);

    const card = findByTestId(root, "card");
    const body = findByTestId(card, "card-body"); // Search *inside* card

    assert.ok(body, "EF_REACT_COMP_NESTING: CardBody must be inside Card");
    assert.equal(body.children[0], "I am the body", "EF_REACT_COMP_TEXT");
});

```

**Workspace Starter**

```javascript
import React from 'react';

export function CardBody() {
    return null;
}

export function Card() {
    return null;
}

```

**Meta**

```json
{
  "slug": "react-components",
  "tier": 1,
  "world": "world-react",
  "readme_path": "data/quests/react-components/workspace/README.md",
  "public_test_path": "data/quests/react-components/grading/public/react-components.public.test.mjs",
  "workspace_paths": [
    "data/quests/react-components/workspace/task.mjs"
  ],
  "run_command": "node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution"
}
```


### Quest Packet: react-props

**README.md**

```md
# React Props: Dynamic Greeting

Edit `task.mjs` to export a component `Welcome`.

Requirements:
1. Accept a prop `name`.
2. Render an `h1` with `data-testid="welcome"`.
3. If `name` is provided, text should be "Hello, {name}!".
4. If `name` is missing (undefined/null), text should be "Hello, Stranger!".

```

**Public Test**

```javascript
import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId } from "../../../_shared/react_test_helpers.mjs";
import { Welcome } from "../../workspace/task.mjs";

test("renders prop name", () => {
    const { root } = runComponent(Welcome, { name: "Alice" });
    const h1 = findByTestId(root, "welcome");
    assert.equal(h1.children[0], "Hello, Alice!", "EF_REACT_PROPS_NAME");
});

test("renders default stranger", () => {
    const { root } = runComponent(Welcome, {});
    const h1 = findByTestId(root, "welcome");
    assert.equal(h1.children[0], "Hello, Stranger!", "EF_REACT_PROPS_DEFAULT");
});

```

**Workspace Starter**

```javascript
import React from 'react';

export function Welcome(props) {
    return null;
}

```

**Meta**

```json
{
  "slug": "react-props",
  "tier": 1,
  "world": "world-react",
  "readme_path": "data/quests/react-props/workspace/README.md",
  "public_test_path": "data/quests/react-props/grading/public/react-props.public.test.mjs",
  "workspace_paths": [
    "data/quests/react-props/workspace/task.mjs"
  ],
  "run_command": "node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution"
}
```


### Quest Packet: react-conditional-render

**README.md**

```md
# React Conditional Render

Edit `task.mjs` to export a component `ToggleSection`.

Requirements:
1. Accept props `title` (string) and `isVisible` (boolean).
2. Always render an `h2` with the `title`.
3. If `isVisible` is true, render a `p` tag with text "Now you see me".
4. If `isVisible` is false, do NOT render the `p` tag.

```

**Public Test**

```javascript
import test from "node:test";
import assert from "node:assert/strict";
import { runComponent } from "../../../_shared/react_test_helpers.mjs";
import { ToggleSection } from "../../workspace/task.mjs";

test("renders title and content when visible", () => {
    const { root } = runComponent(ToggleSection, { title: "Secret", isVisible: true });

    const h2 = root.findByType("h2");
    assert.equal(h2.children[0], "Secret", "EF_REACT_COND_TITLE");

    const p = root.findByType("p");
    assert.equal(p.children[0], "Now you see me", "EF_REACT_COND_VISIBLE");
});

```

**Workspace Starter**

```javascript
import React from 'react';

export function ToggleSection({ title, isVisible }) {
    return React.createElement('div', null,
        React.createElement('h2', null, title)
        // TODO: conditional p tag
    );
}

```

**Meta**

```json
{
  "slug": "react-conditional-render",
  "tier": 1,
  "world": "world-react",
  "readme_path": "data/quests/react-conditional-render/workspace/README.md",
  "public_test_path": "data/quests/react-conditional-render/grading/public/react-conditional-render.public.test.mjs",
  "workspace_paths": [
    "data/quests/react-conditional-render/workspace/task.mjs"
  ],
  "run_command": "node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution"
}
```


### Quest Packet: react-lists

**README.md**

```md
# React Lists: User Directory

Edit `task.mjs` to export a component `UserList`.

Requirements:
1. Accept a prop `users` (array of objects with `id` and `name`).
2. Render a `ul` with `data-testid="user-list"`.
3. Render an `li` for each user.
4. Each `li` MUST have a unique `key` prop set to the user's `id`.
5. The content of the `li` should be the user's `name`.

```

**Public Test**

```javascript
import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { runComponent, findByTestId, readFixture } from "../../../_shared/react_test_helpers.mjs";
import { UserList } from "../../workspace/task.mjs";

const WS = path.resolve(import.meta.dirname, "../../workspace");

test("renders list items with keys", () => {
    const users = readFixture(WS, "fixtures/users.json");
    const { root } = runComponent(UserList, { users });

    const ul = findByTestId(root, "user-list");
    const lis = ul.findAllByType("li");

    assert.equal(lis.length, 3, "EF_REACT_LIST_COUNT");
    assert.equal(lis[0].children[0], "Alice", "EF_REACT_LIST_TEXT");

    // Verify keys - react-test-renderer exposes key on the instance or fiber node usually, 
    // but simpler check is implicitly done by React if we update list.
    // We can check the prop '_store' or similar internal, but cleaner is purely structure.
    // Actually, TestRenderer exposes 'key' property on tree nodes if present? No, it's special.
    // However, we can check if react complains (console.error) but we capture stdout.
    // Ideally, we assume if they map correctly it works.

    // Checking key in react-test-renderer:
    // node.props.key is NOT available. key is separate property on the node object itself.
    // But root.findAllByType('li')[0]._fiber.key could be hacked.
    // Official way: we trust the output structure.
});

```

**Workspace Starter**

```javascript
import React from 'react';

export function UserList({ users }) {
    return React.createElement('ul', { 'data-testid': 'user-list' });
}

```

**Meta**

```json
{
  "slug": "react-lists",
  "tier": 1,
  "world": "world-react",
  "readme_path": "data/quests/react-lists/workspace/README.md",
  "public_test_path": "data/quests/react-lists/grading/public/react-lists.public.test.mjs",
  "workspace_paths": [
    "data/quests/react-lists/workspace/task.mjs"
  ],
  "run_command": "node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution"
}
```


### Quest Packet: react-state-counter

**README.md**

```md
# React State: Counter

Edit `task.mjs` to export a component `Counter`.

Requirements:
1. Render a `div` with `data-testid="count"` displaying the current count (starts at 0).
2. Render a button with `data-testid="increment"` that adds 1 to the count.
3. Render a button with `data-testid="reset"` that sets the count to 0.

Use `React.useState`.

```

**Public Test**

```javascript
import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, act } from "../../../_shared/react_test_helpers.mjs";
import { Counter } from "../../workspace/task.mjs";

test("increments counter", () => {
    const { root } = runComponent(Counter);

    const countDiv = findByTestId(root, "count");
    const btn = findByTestId(root, "increment");

    assert.equal(countDiv.children[0], "0", "EF_REACT_STATE_INIT");

    act(() => {
        btn.props.onClick();
    });

    assert.equal(countDiv.children[0], "1", "EF_REACT_STATE_INC");

    act(() => {
        btn.props.onClick();
    });

    assert.equal(countDiv.children[0], "2", "EF_REACT_STATE_INC_2");
});

```

**Workspace Starter**

```javascript
import React, { useState } from 'react';

export function Counter() {
    const [count, setCount] = useState(0);

    return React.createElement('div', null,
        React.createElement('div', { 'data-testid': 'count' }, /* TODO */),
        React.createElement('button', { 'data-testid': 'increment' }, '+1'),
        React.createElement('button', { 'data-testid': 'reset' }, 'Reset')
    );
}

```

**Meta**

```json
{
  "slug": "react-state-counter",
  "tier": 1,
  "world": "world-react",
  "readme_path": "data/quests/react-state-counter/workspace/README.md",
  "public_test_path": "data/quests/react-state-counter/grading/public/react-state-counter.public.test.mjs",
  "workspace_paths": [
    "data/quests/react-state-counter/workspace/task.mjs"
  ],
  "run_command": "node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution"
}
```


### Quest Packet: react-state-toggle

**README.md**

```md
# React State: Toggle

Edit `task.mjs` to export a component `ToggleButton`.

Requirements:
1. Render a `button` with `data-testid="toggle"`.
2. Initial text should be "OFF".
3. When clicked, text swaps between "OFF" and "ON".

```

**Public Test**

```javascript
import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, act } from "../../../_shared/react_test_helpers.mjs";
import { ToggleButton } from "../../workspace/task.mjs";

test("toggles between ON and OFF", () => {
    const { root } = runComponent(ToggleButton);

    const btn = findByTestId(root, "toggle");
    assert.equal(btn.children[0], "OFF", "EF_REACT_TOGGLE_INIT");

    act(() => btn.props.onClick());
    assert.equal(btn.children[0], "ON", "EF_REACT_TOGGLE_ON");

    act(() => btn.props.onClick());
    assert.equal(btn.children[0], "OFF", "EF_REACT_TOGGLE_OFF");
});

```

**Workspace Starter**

```javascript
import React, { useState } from 'react';

export function ToggleButton() {
    return React.createElement('button', { 'data-testid': 'toggle' }, 'OFF');
}

```

**Meta**

```json
{
  "slug": "react-state-toggle",
  "tier": 1,
  "world": "world-react",
  "readme_path": "data/quests/react-state-toggle/workspace/README.md",
  "public_test_path": "data/quests/react-state-toggle/grading/public/react-state-toggle.public.test.mjs",
  "workspace_paths": [
    "data/quests/react-state-toggle/workspace/task.mjs"
  ],
  "run_command": "node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution"
}
```


### Quest Packet: react-effects-mount

**README.md**

```md
# React Effects: Mount/Unmount

Edit `task.mjs` to export a component `LifecycleLogger`.

Requirements:
1. Accept props `onMount` and `onUnmount` (functions).
2. Use `useEffect` to call `onMount` when the component mounts.
3. Return a cleanup function from the effect that calls `onUnmount`.
4. Render null or any element.

```

**Public Test**

```javascript
import test from "node:test";
import assert from "node:assert/strict";
import { runComponent } from "../../../_shared/react_test_helpers.mjs";
import { LifecycleLogger } from "../../workspace/task.mjs";

test("calls onMount but not onUnmount initially", () => {
    let mounted = 0;
    let unmounted = 0;

    runComponent(LifecycleLogger, {
        onMount: () => mounted++,
        onUnmount: () => unmounted++
    });

    assert.equal(mounted, 1, "EF_REACT_EFFECT_MOUNT");
    assert.equal(unmounted, 0, "EF_REACT_EFFECT_NO_UNMOUNT_YET");
});

```

**Workspace Starter**

```javascript
import React, { useEffect } from 'react';

export function LifecycleLogger({ onMount, onUnmount }) {
    // TODO: Implement useEffect
    return null;
}

```

**Meta**

```json
{
  "slug": "react-effects-mount",
  "tier": 1,
  "world": "world-react",
  "readme_path": "data/quests/react-effects-mount/workspace/README.md",
  "public_test_path": "data/quests/react-effects-mount/grading/public/react-effects-mount.public.test.mjs",
  "workspace_paths": [
    "data/quests/react-effects-mount/workspace/task.mjs"
  ],
  "run_command": "node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution"
}
```


### Quest Packet: react-context-theme

**README.md**

```md
# React Context: Theme

Edit `task.mjs`.

1. Create a Context (not exported).
2. Export `ThemeProvider` component:
   - Accept props `children` and `theme` (string).
   - Render the Context Provider with `value={theme}` surrounding the children.
3. Export `ThemedButton` component:
   - Consume the context `theme`.
   - Render a `button` with `data-testid="btn"`.
   - The button text should be the theme value.

```

**Public Test**

```javascript
import test from "node:test";
import assert from "node:assert/strict";
import React from "react";
import { runComponent, findByTestId } from "../../../_shared/react_test_helpers.mjs";
import { ThemeProvider, ThemedButton } from "../../workspace/task.mjs";

test("button consumes theme from provider", () => {
    // We render Provider -> Button
    // We can't use runComponent directly on just Button if we need wrapper
    // But runComponent takes Component, so we can pass a wrapper component

    const Wrapper = () => React.createElement(
        ThemeProvider,
        { theme: "dark" },
        React.createElement(ThemedButton)
    );

    const { root } = runComponent(Wrapper);
    const btn = findByTestId(root, "btn");

    assert.equal(btn.children[0], "dark", "EF_REACT_CONTEXT_CONSUME");
});

```

**Workspace Starter**

```javascript
import React, { createContext, useContext } from 'react';

const ThemeContext = createContext('light');

export function ThemeProvider({ children, theme }) {
    // TODO: Provider
    return React.createElement(React.Fragment, null, children);
}

export function ThemedButton() {
    // TODO: useContext
    return React.createElement('button', { 'data-testid': 'btn' }, 'default');
}

```

**Meta**

```json
{
  "slug": "react-context-theme",
  "tier": 1,
  "world": "world-react",
  "readme_path": "data/quests/react-context-theme/workspace/README.md",
  "public_test_path": "data/quests/react-context-theme/grading/public/react-context-theme.public.test.mjs",
  "workspace_paths": [
    "data/quests/react-context-theme/workspace/task.mjs"
  ],
  "run_command": "node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution"
}
```


### Quest Packet: react-reducer-cart

**README.md**

```md
# React Reducer: Shopping Cart

Edit `task.mjs` to export `ShoppingCart`.

Requirements:
1. Use `useReducer` to manage state. Initial state: `{ total: 0 }`.
2. Render a `div` with `data-testid="total"` showing the current total.
3. Render a button with `data-testid="add-10` that adds 10 to the total.
4. Render a button with `data-testid="reset"` that resets total to 0.

Actions should roughly be `{ type: 'ADD', amount: 10 }` and `{ type: 'RESET' }`.

```

**Public Test**

```javascript
import test from "node:test";
import assert from "node:assert/strict";
import { runComponent, findByTestId, act } from "../../../_shared/react_test_helpers.mjs";
import { ShoppingCart } from "../../workspace/task.mjs";

test("adds values to total", () => {
    const { root } = runComponent(ShoppingCart);
    const total = findByTestId(root, "total");
    const add10 = findByTestId(root, "add-10");

    assert.equal(total.children[0], "0", "EF_REACT_REDUCER_INIT");

    act(() => add10.props.onClick());
    assert.equal(total.children[0], "10", "EF_REACT_REDUCER_ADD");

    act(() => add10.props.onClick());
    assert.equal(total.children[0], "20", "EF_REACT_REDUCER_ADD_2");
});

```

**Workspace Starter**

```javascript
import React, { useReducer } from 'react';

const initialState = { total: 0 };

function reducer(state, action) {
    // TODO: implement reducer logic
    return state;
}

export function ShoppingCart() {
    const [state, dispatch] = useReducer(reducer, initialState);

    return React.createElement('div', null,
        React.createElement('div', { 'data-testid': 'total' }, state.total),
        React.createElement('button', { 'data-testid': 'add-10' }, '+10'),
        React.createElement('button', { 'data-testid': 'reset' }, 'Reset')
    );
}

```

**Meta**

```json
{
  "slug": "react-reducer-cart",
  "tier": 1,
  "world": "world-react",
  "readme_path": "data/quests/react-reducer-cart/workspace/README.md",
  "public_test_path": "data/quests/react-reducer-cart/grading/public/react-reducer-cart.public.test.mjs",
  "workspace_paths": [
    "data/quests/react-reducer-cart/workspace/task.mjs"
  ],
  "run_command": "node scripts/run_world_public_tests.mjs --questpack data/questpacks/react_core.json --mode solution"
}
```


React quest packets complete: 9/9 sent.
