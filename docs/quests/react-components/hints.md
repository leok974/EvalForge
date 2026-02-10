# Hints — React Components: Composition

## Hint 1 (nudge)
Build the inside piece first (`CardBody`), then wrap it (`Card`).

## Hint 2 (more specific)
The test does:
- find `"card"`
- then searches **inside card** for `"card-body"`

So `Card` must render `CardBody` as its child.

## Hint 3 (close)
`CardBody`:
- `React.createElement("div", { "data-testid": "card-body" }, "I am the body")`

`Card`:
- `React.createElement("div", { "data-testid": "card" }, React.createElement(CardBody))`
