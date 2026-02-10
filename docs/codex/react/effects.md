# Effects

The `useEffect` Hook lets you perform side effects in function components. Data fetching, setting up a subscription, and manually changing the DOM in React components are all examples of side effects.

## Example

```javascript
import { useEffect } from 'react';

useEffect(() => {
  // Update the document title using the browser API
  document.title = `You clicked ${count} times`;
});
```

## Cleanup

If your effect returns a function, React will run it when it is time to clean up.
