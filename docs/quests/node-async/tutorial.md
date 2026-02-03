# Async Patterns: Promises, async/await, Errors

## Outcome

Write async code with correct error handling.

## Core concepts

async/await, promise rejection, try/catch.

## Mental model

errors must propagate as rejections; you must await or handle.

## Walkthrough

read file async, fetch-like async, wrap in try/catch.

## Practice

implement `run()` that returns non-zero on failure.

## Common pitfalls

forgetting `await`, unhandled promise rejections.

## Check yourself

Why can a promise fail “silently” if you don’t await?

