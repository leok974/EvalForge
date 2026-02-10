# State

State is a built-in React object that is closely related to props. State allows React components to change their output over time in response to user actions, network responses, and anything else, without violating the rule that components must be pure with respect to their props.

## useState Hook

`useState` is a Hook that lets you add React state to function components.

```javascript
import { useState } from 'react';

function Example() {
  // Declare a new state variable, which we'll call "count"
  const [count, setCount] = useState(0);
```
