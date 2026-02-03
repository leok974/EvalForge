# HTTP Server: Routes and JSON

## Outcome

Serve JSON with status codes and simple routing.

## Core concepts

request/response, headers, status codes, JSON.

## Mental model

server is a function from request → response.

## Walkthrough

`/health`, `/hello`, 404 fallback.

## Practice

implement `/echo` that returns parsed JSON safely.

## Common pitfalls

not ending response, wrong content-type.

## Check yourself

When should you return 400 vs 500?

