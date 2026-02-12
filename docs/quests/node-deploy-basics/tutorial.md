# Tutorial — node-deploy-basics

## What You’re Practicing
- production conventions (`npm start`)
- runtime configuration via `process.env.PORT`
- health checks used by load balancers and orchestration systems

## Implementation Plan
1) Update `package.json`:
- add `"scripts": { "start": "node app.js" }`

2) Update `app.js`:
- set `PORT` using `process.env.PORT ?? 3000`
- implement `/healthz` returning `OK`

## Pitfalls
- forgetting `PORT` is a string (convert to number if you want)
- returning the wrong body (`"Ok"` vs `"OK"`)
- changing the startup log format (tests look for the port)
