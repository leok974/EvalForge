# Deploy Basics

Preparing for production means health checks and standard scripts.

## Goal
1.  **package.json**: Add a `"start"` script: `"node app.js"`.
2.  **app.js**:
    *   Bind to `process.env.PORT` (or default to 3000).
    *   Implement `GET /healthz` returning 200 "OK".

## Verification
`npm start` should work.
Accessing `/healthz` should return "OK".
