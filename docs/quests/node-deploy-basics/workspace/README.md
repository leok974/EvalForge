# Deploy Basics

Preparing for production means standard scripts and health checks.

## Goal
1) **package.json**
- Add a `"start"` script that runs: `node app.js`

2) **app.js**
- Bind to `process.env.PORT` (default to `3000`)
- Implement `GET /healthz` returning status `200` and body `OK`

## Verification
- `npm start` should work
- `GET /healthz` should return `OK`
