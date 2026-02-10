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
