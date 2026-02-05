# World React: Foundations

Welcome to the React world! In this world, you will learn the core mechanics of React: Components, Props, State, Effects, Context, and Reducers.

## Pure JavaScript (No JSX)

To focus on how React actually works "under the hood" and to simplify the environment (no build steps, no Babel), **we will not use JSX** in this tier.

Instead, you will use `React.createElement`.

### `React.createElement` Cheatsheet

```javascript
// JSX: <div className="box">Hello</div>
React.createElement('div', { className: 'box' }, 'Hello')

// JSX: <MyComponent name="Alice" />
React.createElement(MyComponent, { name: 'Alice' })

// JSX: 
// <div>
//   <h1>Title</h1>
//   <p>Body</p>
// </div>
React.createElement('div', null,
  React.createElement('h1', null, 'Title'),
  React.createElement('p', null, 'Body')
)
```

### Why?
1. **Understanding**: JSX is just syntactic sugar. Knowing `createElement` helps you debug component trees.
2. **Speed**: No build step means instant feedback.
3. **Simplicity**: You only need Node.js.

## Quests

1. **Ignition**: Render your first element.
2. **Components**: Compose functions.
3. **Props**: Pass data.
4. **Logic**: Conditional rendering.
5. **Lists**: Keys and mapping.
6. **State**: `useState`.
7. **Effects**: `useEffect`.
8. **Context**: `createContext`.
9. **Reducers**: `useReducer`.
