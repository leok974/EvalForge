# Middleware: Logging, Errors, Request IDs

## Outcome

Add logging + error handling + request IDs.

## Core concepts

middleware pipeline, correlation ID, structured logs.

## Mental model

middleware wraps your handler; errors funnel to one place.

## Walkthrough

add request-id header + log start/end + error handler.

## Practice

emit consistent JSON logs for each request.

## Common pitfalls

logging secrets, losing stack traces.

## Check yourself

Why do request IDs matter?

