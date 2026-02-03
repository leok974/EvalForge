# Environment & Secrets

Edit `check_env.js` to:

* default `MODE` to `dev` if missing/empty
* default `PORT` to `3000` if missing/empty
* require `API_KEY` (non-empty) or exit **code 3**
* print exactly:

  * `MODE=...`
  * `PORT=...`
  * `API_KEY=SET` or `API_KEY=MISSING`
