# Briefing — node-deploy-basics

## Objective
Make this project “deploy-ready” by following two conventions:
- `npm start` runs your app
- `/healthz` confirms the service is alive

## Contract
- Start script: `node app.js`
- Port: `process.env.PORT` (default `3000`)
- `GET /healthz` → 200 + `OK`

## Success Criteria
Public tests pass.
